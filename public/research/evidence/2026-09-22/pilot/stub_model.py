"""Deterministic model driver. Ordinal is kept in the EXTERNAL world db, never readable
by the runtime under test. A repeated call returns a DIFFERENT answer, so that any
regeneration after resume is observable."""
RESPONSES = [
    {"proposal_id": "A", "tool": "write", "payload": "ALPHA",   "decision": "A"},
    {"proposal_id": "B", "tool": "write", "payload": "BETA",    "decision": "B"},
    {"proposal_id": "C", "tool": "write", "payload": "GAMMA",   "decision": "C"},
    {"proposal_id": "D", "tool": "write", "payload": "DELTA",   "decision": "D"},
]

class StubModel:
    def __init__(self, world, log, logical_run_id):
        self.w, self.log, self.run = world, log, logical_run_id
    def call(self):
        n = self.w.bump(f"model_ordinal:{self.run}")
        r = dict(RESPONSES[min(n, len(RESPONSES)) - 1])
        self.log.emit(type="model.call", logical_run_id=self.run,
                      ordinal_global=n, response_id=r["proposal_id"])
        return r
