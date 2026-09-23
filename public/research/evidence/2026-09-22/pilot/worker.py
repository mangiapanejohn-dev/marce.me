"""One phase of one logical run, in its own interpreter. Killed externally at the fault point."""
import argparse, importlib, os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pilot.world import World
from pilot.eventlog import EventLog
from pilot.stub_model import StubModel
from pilot.adapters.base import Ctx

ADAPTERS = {
    "broken-control": ("pilot.adapters.broken_control", "BrokenControl"),
    "correct-control": ("pilot.adapters.correct_control", "CorrectControl"),
    "langgraph": ("pilot.adapters.langgraph_adapter", "LangGraphAdapter"),
    "openai-agents": ("pilot.adapters.openai_agents_adapter", "OpenAIAgentsAdapter"),
    "pydantic-ai": ("pilot.adapters.pydantic_ai_adapter", "PydanticAIAdapter"),
    "temporal": ("pilot.adapters.temporal_adapter", "TemporalAdapter"),
}

def main():
    ap = argparse.ArgumentParser()
    for k in ("adapter", "probe", "run", "dir"): ap.add_argument("--" + k, required=True)
    ap.add_argument("--phase", type=int, required=True)
    ap.add_argument("--budget", type=int, default=3)
    a = ap.parse_args()
    mod, cls = ADAPTERS[a.adapter]
    adapter = getattr(importlib.import_module(mod), cls)()
    world = World(os.path.join(a.dir, "world.sqlite"))
    log = EventLog(os.path.join(a.dir, "events.jsonl"))
    stub = StubModel(world, log, a.run)
    ctx = Ctx(world, log, stub, a.run, a.phase, None,
              os.path.join(a.dir, "marker"), a.dir, a.budget)
    log.emit(type="phase.start", logical_run_id=a.run, phase=a.phase, adapter=adapter.name)
    {"C2-R": adapter.run_c2r, "C3-W": adapter.run_c3w, "C3-C": adapter.run_c3c,
     "C2-T": getattr(adapter, "run_c2t", None), "C2-N": getattr(adapter, "run_c2n", None),
     "C2-NI": getattr(adapter, "run_c2ni", None),
     "C1-RV": getattr(adapter, "run_c1rv", None),
     "C1-RAW": getattr(adapter, "run_c1raw", None)}[a.probe](ctx)
    log.emit(type="phase.end", logical_run_id=a.run, phase=a.phase)

if __name__ == "__main__":
    main()
