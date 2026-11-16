"""B: bounded read-only ReAct controller with seeded MockLLM accounting."""
SHAPE = "single"

from lab8.db import connect
from lab8.durability import issue_refund
from lab8.mock_llm import complete
from lab8.schemas import Budget, RunResult, make_run_id
from lab8.shapes.common import finish
from lab8.tools import get_claim_view, lookup_order, compute_compensation, tool_cost
from lab8.trace import Trace


def run_claim(claim_id: str, *, seed: int, store_path: str, crash_at: str | None = None) -> RunResult:
    conn = connect(store_path)
    try:
        return _run(conn, claim_id, seed=seed, crash_at=crash_at)
    finally:
        conn.close()


def _run(conn, claim_id, *, seed, crash_at, draft=True):
    budget = Budget()
    trace = Trace(make_run_id(SHAPE, claim_id, seed))

    def done(status, proposal=0, reason=None):
        if draft:
            # Fixed safe facts only: no raw ticket, parent secret, PII or headers.
            complete(budget, seed=seed, purpose="draft", prompt=f"status={status};proposal={proposal}")
            trace.add("model", {"purpose": "draft"})
        trace.add("decision", {"status": status, "proposal_amount": proposal, "reason": reason})
        return finish(conn, shape=SHAPE, claim_id=claim_id, seed=seed,
                      status=status, proposal_amount=proposal, budget=budget,
                      trace=trace, error_reason=reason)

    budget.add_tool(tool_cost())
    claim = get_claim_view(conn, claim_id)
    trace.add("claim", {"found": claim["found"], "has_order_id": bool(claim.get("order_id"))})
    if not claim["found"]:
        return done("failed", reason="unknown_claim")
    if not claim.get("order_id"):
        return done("needs_info", reason="missing_order_id")
    from lab8.runtime import run_react
    evidence = {}

    def decide(observation):
        # MockLLM emits acknowledgements, not executable tool JSON. This bounded
        # controller maps observations to tools; it does not claim real reasoning.
        last = observation.get("last_tool")
        if last:
            evidence[last] = observation["last_result"]
            trace.add("observation", {"tool": last, "result": observation["last_result"]})
        complete(budget, seed=seed, purpose="plan", prompt=f"read_only;last_tool={last or 'start'}")
        trace.add("model", {"purpose": "plan", "last_tool": last})
        if "lookup_order" not in evidence:
            return {"tool": "lookup_order", "args": {"order_id": claim["order_id"], "principal_id": claim["principal_id"]}}
        if not evidence["lookup_order"].get("visible"):
            return {"final": {"status": "escalated"}}
        if "lookup_policy" not in evidence:
            return {"tool": "lookup_policy", "args": {}}
        if "compute_compensation" not in evidence:
            return {"tool": "compute_compensation", "args": {"order": evidence["lookup_order"]["order"]}}
        return {"final": {"status": "ready"}}

    loop = run_react(conn, budget, observation={"claim": {"claim_id": claim_id}},
                     decide=decide, max_steps=8, worker=True)
    trace.add("react_stop", {"stopped": loop["stopped"], "max_steps": 8})
    if loop["stopped"] != "final":
        return done("failed", reason="step_cap")
    view = evidence.get("lookup_order", {})
    if not view.get("visible"):
        return done("escalated", reason=view.get("reason"))
    quote_payload = evidence["compute_compensation"]
    proposal = int(quote_payload["amount_vnd"])
    trace.add("quote", quote_payload)
    if proposal <= 0:
        return done("denied", reason=quote_payload.get("reason"))
    # Full entitlement, not a net amount. Host owns approval and per-order caps.
    # Deliberately propagate InjectedCrash; finally in run_claim closes SQLite.
    outcome = issue_refund(conn, claim_id, proposal, crash_at=crash_at)
    trace.add("host", {"ok": outcome["ok"], "reason": outcome["reason"]})
    status = "resolved" if outcome["ok"] else ("failed" if outcome["conflict"] else "denied")
    return done(status, proposal, None if outcome["ok"] else outcome["reason"])
