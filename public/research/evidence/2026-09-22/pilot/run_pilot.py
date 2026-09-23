"""Parent process: launches a worker, waits for the announced fault point, SIGKILLs it,
then resumes in a fresh interpreter and asks the oracle for a verdict."""
import argparse, hashlib, importlib, json, os, shutil, signal, subprocess, sys, time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pilot.world import World
from pilot.eventlog import EventLog
from pilot.oracle import JUDGES, FROZEN

ROOT = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(ROOT, "results")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 16), b""): h.update(b)
    return h.hexdigest()


def one_attempt(adapter_name, probe, attempt, budget=3, timeout=60):
    run = f"{adapter_name}:{probe}:{attempt}"
    d = os.path.join(RESULTS, "runs", run.replace(":", "_"))
    shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    marker = os.path.join(d, "marker")
    env = dict(os.environ, PYTHONPATH=os.path.dirname(ROOT))

    # ---- phase 1: run until the worker announces the fault point, then SIGKILL ----
    p1 = subprocess.Popen([sys.executable, "-m", "pilot.worker", "--adapter", adapter_name,
                           "--probe", probe, "--run", run, "--dir", d, "--phase", "1",
                           "--budget", str(budget)],
                          cwd=os.path.dirname(ROOT), env=env,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    single_phase = probe.startswith('C1')
    t0 = time.time(); killed = False
    while (not single_phase) and time.time() - t0 < timeout:
        if os.path.exists(marker):
            os.kill(p1.pid, signal.SIGKILL); killed = True; break
        if p1.poll() is not None: break
        time.sleep(0.02)
    out1, err1 = p1.communicate()
    fault_kill = {"killed_by_parent": killed, "phase1_returncode": p1.returncode,
                  "phase1_stderr_tail": err1.decode()[-400:]}

    # ---- phase 2: fresh interpreter, resume the same logical run ----
    log = EventLog(os.path.join(d, "events.jsonl"))
    if probe == "C3-W":                      # the human approves what was PRESENTED
        pres = [e for e in log.read() if e["type"] == "proposal.presented"]
        if pres:
            log.emit(type="approval.granted", logical_run_id=run,
                     for_proposal_id=pres[-1]["proposal_id"], granted_by="harness-operator")
    p2 = None if single_phase else subprocess.run([sys.executable, "-m", "pilot.worker", "--adapter", adapter_name,
                         "--probe", probe, "--run", run, "--dir", d, "--phase", "2",
                         "--budget", str(budget)],
                        cwd=os.path.dirname(ROOT), env=env, capture_output=True, timeout=timeout)

    events = log.read()
    world = World(os.path.join(d, "world.sqlite"))
    outcome, reason, facts = JUDGES[probe](events, world, run, budget)
    oracle_raw_outcome = outcome
    mod, cls = {"broken-control": ("pilot.adapters.broken_control", "BrokenControl"),
                "correct-control": ("pilot.adapters.correct_control", "CorrectControl"),
                "langgraph": ("pilot.adapters.langgraph_adapter", "LangGraphAdapter"),
                "openai-agents": ("pilot.adapters.openai_agents_adapter", "OpenAIAgentsAdapter"),
                "pydantic-ai": ("pilot.adapters.pydantic_ai_adapter", "PydanticAIAdapter"),
                "temporal": ("pilot.adapters.temporal_adapter", "TemporalAdapter")}[adapter_name]
    ad = getattr(importlib.import_module(mod), cls)()
    notes = ad.contract_notes(probe) if hasattr(ad, 'contract_notes') else {}
    if notes.get('contract_relation') == 'explicitly-outside-guarantee':
        outcome, reason = 'inapplicable', (
            'runtime explicitly places this window outside its guarantee; '
            f'raw oracle said {oracle_raw_outcome}: {reason}')
    assert outcome in FROZEN, outcome
    row = dict(study="agent-runtime-invariants-pilot",
               timestamp=time.strftime("%Y-%m-%dT%H:%M:%S"),
               runtime=ad.name, runtime_version=ad.version, population_role=ad.population_role,
               probe=probe, card=probe.split("-")[0], attempt=attempt, logical_run_id=run,
               persistence_backend=ad.applicability().get("persistence_backend"),
               fault_point={"C2-R": "AT_WAIT", "C3-W": "AT_WAIT",
                           "C3-C": "AFTER_CHECKPOINT_BEFORE_WAIT",
                           "C2-T": "AFTER_ACK_BEFORE_NEXT_STEP",
                           "C2-N": "AFTER_EFFECT_COMMIT_BEFORE_ACK",
                           "C2-NI": "AFTER_EFFECT_COMMIT_BEFORE_ACK",
                           "C1-RV": "AT_WAIT_FOREIGN_MUTATION",
                           "C1-RAW": "AT_WAIT_FOREIGN_MUTATION"}[probe],
               positive_control=(adapter_name == "broken-control"),
               negative_control=(adapter_name == "correct-control"),
               budget_initial=budget, outcome=outcome, reason=reason,
               phase2_returncode=(None if p2 is None else p2.returncode),
               phase2_stderr_tail=('' if p2 is None else p2.stderr.decode()[-400:]),
               **fault_kill, **facts,
               oracle_raw_outcome=oracle_raw_outcome,
               **(ad.contract_notes(probe) if hasattr(ad, 'contract_notes') else {}),
               manifest={os.path.basename(f): sha(os.path.join(d, f))
                         for f in sorted(os.listdir(d)) if os.path.isfile(os.path.join(d, f))})
    with open(os.path.join(RESULTS, "rows.jsonl"), "a") as fh:
        fh.write(json.dumps(row, sort_keys=True, default=str) + "\n")
    return row


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--adapter", required=True); ap.add_argument("--probe", required=True)
    ap.add_argument("--attempts", type=int, default=3); ap.add_argument("--budget", type=int, default=3)
    a = ap.parse_args()
    for i in range(1, a.attempts + 1):
        r = one_attempt(a.adapter, a.probe, i, a.budget)
        print(f"{r['runtime']:16s} {r['probe']:5s} att{i}  {r['outcome']:16s} "
              f"killed={r['killed_by_parent']} effects={r['committed_effects']} "
              f"models={r['model_responses']}  {r['reason'][:70]}")
