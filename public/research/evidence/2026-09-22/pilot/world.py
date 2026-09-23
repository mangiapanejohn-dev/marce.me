"""External world: survives process death, independent of any runtime checkpoint store."""
import json, os, sqlite3, time

def _locked(fn):
    def w(self, *a, **k):
        with self._lock:
            return fn(self, *a, **k)
    return w


DDL = """
CREATE TABLE IF NOT EXISTS effects(
  effect_id TEXT PRIMARY KEY, logical_run_id TEXT NOT NULL, proposal_id TEXT NOT NULL,
  payload TEXT NOT NULL, committed_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS counters(key TEXT PRIMARY KEY, value INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS idem(key TEXT PRIMARY KEY, effect_id TEXT NOT NULL,
  result TEXT NOT NULL, first_committed_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS resources(id TEXT PRIMARY KEY, version INTEGER NOT NULL,
  protected INTEGER NOT NULL);
"""

class World:
    def __init__(self, path):
        self.path = path
        self._lock = __import__("threading").RLock()
        self.c = sqlite3.connect(path, isolation_level=None, timeout=30, check_same_thread=False)
        self.c.executescript(DDL)

    @_locked
    def commit(self, logical_run_id, proposal_id, payload, effect_id=None):
        n = self.bump(f"effect_seq:{logical_run_id}")
        eid = effect_id or f"{logical_run_id}:e{n}"
        try:
            self.c.execute("INSERT INTO effects VALUES(?,?,?,?,?)",
                           (eid, logical_run_id, proposal_id, json.dumps(payload),
                            time.strftime("%Y-%m-%dT%H:%M:%S")))
            return {"effect_id": eid, "deduped": False}
        except sqlite3.IntegrityError:
            return {"effect_id": eid, "deduped": True}

    @_locked
    def lookup(self, effect_id):
        r = self.c.execute("SELECT * FROM effects WHERE effect_id=?", (effect_id,)).fetchone()
        return r

    @_locked
    def count_effects(self, logical_run_id):
        return self.c.execute("SELECT COUNT(*) FROM effects WHERE logical_run_id=?",
                              (logical_run_id,)).fetchone()[0]

    @_locked
    def effects(self, logical_run_id):
        return [dict(effect_id=r[0], proposal_id=r[2], payload=json.loads(r[3]))
                for r in self.c.execute(
                    "SELECT * FROM effects WHERE logical_run_id=? ORDER BY rowid", (logical_run_id,))]

    @_locked
    def bump(self, key):
        self.c.execute("INSERT INTO counters VALUES(?,0) ON CONFLICT(key) DO NOTHING", (key,))
        self.c.execute("UPDATE counters SET value=value+1 WHERE key=?", (key,))
        return self.c.execute("SELECT value FROM counters WHERE key=?", (key,)).fetchone()[0]

    @_locked
    def put_resource(self, rid, version, protected):
        self.c.execute("INSERT INTO resources VALUES(?,?,?) ON CONFLICT(id) DO UPDATE SET "
                       "version=?, protected=?", (rid, version, int(protected), version, int(protected)))

    @_locked
    def get_resource(self, rid):
        r = self.c.execute("SELECT version, protected FROM resources WHERE id=?", (rid,)).fetchone()
        return None if r is None else {"version": r[0], "protected": bool(r[1])}

    @_locked
    def idem_lookup(self, key):
        r = self.c.execute("SELECT effect_id, result FROM idem WHERE key=?", (key,)).fetchone()
        return None if r is None else {"effect_id": r[0], "result": r[1]}

    @_locked
    def idem_commit(self, logical_run_id, key, payload, result):
        """Atomic check-and-commit against the application-supplied idempotency key.

        Returns (effect_id, reused: bool). The uniqueness of `key` is enforced by the
        store, not by the caller, so a concurrent or retried caller cannot double-commit.
        """
        prev = self.c.execute("SELECT effect_id, result FROM idem WHERE key=?", (key,)).fetchone()
        if prev is not None:
            return prev[0], True
        eid = f"{logical_run_id}:idem:{key[:40]}"
        self.c.execute("BEGIN IMMEDIATE")
        try:
            self.c.execute("INSERT INTO idem VALUES(?,?,?,datetime('now'))", (key, eid, result))
            self.c.execute("INSERT INTO effects VALUES(?,?,?,?,datetime('now'))",
                           (eid, logical_run_id, key, payload))
            self.c.execute("COMMIT")
        except Exception:
            self.c.execute("ROLLBACK")
            prev = self.c.execute("SELECT effect_id, result FROM idem WHERE key=?", (key,)).fetchone()
            if prev is None:
                raise
            return prev[0], True
        return eid, False
