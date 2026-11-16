"""B4 rules-only baseline: same workflow, no draft/model call."""
from lab8.db import connect
from lab8.shapes.workflow import _run


def run_claim(claim_id, *, seed, store_path, crash_at=None):
    conn = connect(store_path)
    try:
        return _run(conn, claim_id, seed=seed, crash_at=crash_at,
                    draft=False, shape="rules_only")
    finally:
        conn.close()
