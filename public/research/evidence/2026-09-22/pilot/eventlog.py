"""Append-only external event stream. The oracle reads ONLY this plus the world DB."""
import json, os, time

class EventLog:
    def __init__(self, path): self.path = path
    def emit(self, **rec):
        rec.setdefault("ts", time.time()); rec.setdefault("process_id", os.getpid())
        with open(self.path, "a") as fh:
            fh.write(json.dumps(rec, sort_keys=True) + "\n"); fh.flush(); os.fsync(fh.fileno())
    def read(self):
        if not os.path.exists(self.path): return []
        return [json.loads(l) for l in open(self.path) if l.strip()]
