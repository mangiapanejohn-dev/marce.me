"""Verdicts are computed ONLY from the external event stream and the external world DB.
No runtime internals, no runtime self-report, no source reading."""

FROZEN = {"violated", "not-violated", "NOT-CAPTURED", "probe-insensitive", "inapplicable"}


def _pids(events):
    return sorted({e.get("process_id") for e in events if e.get("process_id")})


def base_facts(events, world, run_id):
    return dict(
        fault_reached=any(e["type"] == "faultpoint.reached" for e in events),
        fresh_process_resume=len(_pids(events)) >= 2,
        model_calls_global=sum(1 for e in events if e["type"] == "model.call"),
        model_responses=[e["response_id"] for e in events if e["type"] == "model.call"],
        committed_effects=world.count_effects(run_id),
        tool_invocations=sum(1 for e in events if e["type"] == "effect.committed"),
    )


def judge_c2r(events, world, run_id, budget):
    f = base_facts(events, world, run_id)
    eff = world.effects(run_id)
    f["budget_replayed"] = (f["committed_effects"] > budget) or any(
        e["type"] == "budget.reset_on_resume" for e in events)
    f["duplicate_external_effect"] = len({e["proposal_id"] for e in eff}) < len(eff)
    f["evidence_complete"] = f["fault_reached"] and f["fresh_process_resume"]
    if not f["evidence_complete"]:
        return "NOT-CAPTURED", "fault point or fresh-process resume not observed", f
    if f["committed_effects"] > budget:
        return "violated", f"{f['committed_effects']} committed effects for budget {budget}", f
    return "not-violated", f"{f['committed_effects']} <= budget {budget}", f


def judge_c3w(events, world, run_id, budget):
    f = base_facts(events, world, run_id)
    pres = [e for e in events if e["type"] == "proposal.presented"]
    appr = [e for e in events if e["type"] == "approval.granted"]
    eff = world.effects(run_id)
    f["approved_proposal_id"] = appr[-1]["for_proposal_id"] if appr else None
    f["dispatched_proposal_id"] = eff[-1]["proposal_id"] if eff else None
    f["unnecessary_regeneration"] = any(e["type"] == "proposal.regenerated" for e in events)
    f["semantic_mismatch"] = bool(
        f["approved_proposal_id"] and f["dispatched_proposal_id"]
        and f["approved_proposal_id"] != f["dispatched_proposal_id"])
    f["evidence_complete"] = bool(pres and appr and eff and f["fault_reached"]
                                  and f["fresh_process_resume"])
    if not f["evidence_complete"]:
        return "NOT-CAPTURED", "missing presentation, approval, effect, or fresh-process resume", f
    if f["semantic_mismatch"]:
        return "violated", (f"approval was for {f['approved_proposal_id']} but "
                            f"{f['dispatched_proposal_id']} was dispatched with no new approval"), f
    return "not-violated", f"dispatched the approved proposal {f['approved_proposal_id']}", f


def judge_c3c(events, world, run_id, budget):
    f = base_facts(events, world, run_id)
    eff = world.effects(run_id)
    first = [e for e in events if e["type"] == "decision.recorded"]
    f["decision_before_fault"] = first[0]["decision"] if first else None
    f["tool_after_resume"] = eff[-1]["payload"] if eff else None
    f["unnecessary_regeneration"] = any(e["type"] == "decision.regenerated" for e in events)
    expected = {"A": "toolX"}.get(f["decision_before_fault"], "toolY")
    f["semantic_mismatch"] = bool(f["tool_after_resume"] and f["tool_after_resume"] != expected)
    f["evidence_complete"] = bool(first and eff and f["fault_reached"] and f["fresh_process_resume"])
    if not f["evidence_complete"]:
        return "NOT-CAPTURED", "missing pre-fault decision, effect, or fresh-process resume", f
    if f["semantic_mismatch"]:
        return "violated", (f"pre-fault decision {f['decision_before_fault']} implies {expected} "
                            f"but {f['tool_after_resume']} was dispatched"), f
    return "not-violated", f"branch after resume matches pre-fault decision ({expected})", f


def judge_c1(events, world, run_id, budget):
    f = base_facts(events, world, run_id)
    vals = [e for e in events if e["type"] == "validation.invoked"]
    mut = [e for e in events if e["type"] == "foreign.mutation"]
    appr = [e for e in events if e["type"] == "approval.granted"]
    eff = world.effects(run_id)
    f["validation_calls"] = len(vals)
    f["validation_world_versions"] = [v.get("world_version") for v in vals]
    f["validation_decisions"] = [v.get("decision") for v in vals]
    f["approval_call_id"] = appr[-1].get("for_call_id") if appr else None
    f["executed_call_id"] = eff[-1]["proposal_id"] if eff else None
    f["foreign_mutation_observed"] = bool(mut)
    f["destructive_effects"] = len(eff)
    post = [v for v in vals if v.get("after_mutation")]
    f["revalidated_after_mutation"] = bool(post)
    f["evidence_complete"] = bool(vals and mut and appr)
    if not f["evidence_complete"]:
        return "NOT-CAPTURED", "missing validation, foreign mutation, or approval record", f
    if f["destructive_effects"] > 0:
        return "violated", (f"effect dispatched after the world moved to version "
                            f"{mut[-1].get('to_version')} (protected="
                            f"{mut[-1].get('to_protected')}); validations saw versions "
                            f"{f['validation_world_versions']}"), f
    if not f["revalidated_after_mutation"]:
        # no effect, but no post-mutation validation either: cannot tell revalidation
        # apart from the action simply never being attempted
        return "NOT-CAPTURED", ("no destructive effect, but no validation was invoked after the "
                                "foreign mutation, so revalidation cannot be distinguished from "
                                "the action never being re-attempted"), f
    return "not-violated", (f"revalidated against the post-mutation world "
                            f"(versions {f['validation_world_versions']}, decisions "
                            f"{f['validation_decisions']}) and dispatched nothing"), f


def judge_c2ni(events, world, run_id, budget):
    """Delegated Obligation Closure. Three capability conditions, all judged from the
    external event stream and the external store only."""
    f = base_facts(events, run_id=run_id, world=world) if False else base_facts(events, world, run_id)
    reads = [e for e in events if e["type"] == "execution_info.read"]
    looks = [e for e in events if e["type"] == "idem.lookup"]
    commits = [e for e in events if e["type"] == "effect.committed"]
    reuses = [e for e in events if e["type"] == "effect.reused"]
    keys = [e.get("idempotency_key") for e in reads]
    pids = sorted({e.get("attempt_pid") for e in reads if e.get("attempt_pid")})
    f["attempts_observed"] = len(reads)
    f["attempt_pids"] = pids
    f["effect_keys"] = keys
    f["key_mode"] = reads[0].get("key_mode") if reads else None
    f["execution_info_snapshot"] = {k: v for k, v in (reads[0].items() if reads else [])
                                    if k.startswith("ei_")}
    f["external_effect_count"] = world.count_effects(run_id)
    # --- the three capability conditions ---
    f["stable_identity"] = bool(keys) and len(set(keys)) == 1 and len(reads) >= 2
    f["boundary_access"] = bool(looks) and all(e.get("before_effect") for e in looks) \
        and len(looks) >= len(commits)
    f["durable_reconciliation"] = bool(reuses) or (len(looks) >= 2 and
                                                  any(e.get("hit") for e in looks))
    f["obligation_dischargeable"] = bool(f["stable_identity"] and f["boundary_access"]
                                         and f["durable_reconciliation"])
    f["evidence_complete"] = bool(f["fault_reached"] and f["fresh_process_resume"]
                                  and len(reads) >= 2)
    if not f["evidence_complete"]:
        return "NOT-CAPTURED", ("the retry window was not exercised: need a fault, a "
                                "fresh-process resume, and at least two task attempts"), f
    if f["external_effect_count"] > 1:
        return "violated", (f"{f['external_effect_count']} external effects across "
                            f"{len(pids)} processes; keys used {keys}"), f
    if not f["obligation_dischargeable"]:
        return "NOT-CAPTURED", ("exactly one external effect, but not all three capability "
                                f"conditions hold (stable_identity={f['stable_identity']}, "
                                f"boundary_access={f['boundary_access']}, "
                                f"durable_reconciliation={f['durable_reconciliation']})"), f
    return "not-violated", ("the application discharged the delegated obligation using only "
                            f"public API: one external effect across {len(pids)} processes, "
                            f"identical key on every attempt"), f


JUDGES = {"C2-R": judge_c2r, "C3-W": judge_c3w, "C3-C": judge_c3c,
          "C2-T": judge_c2r, "C2-N": judge_c2r,
          "C1-RV": judge_c1, "C1-RAW": judge_c1,
          "C2-NI": judge_c2ni}
