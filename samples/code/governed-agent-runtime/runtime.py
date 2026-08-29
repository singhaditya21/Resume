"""A compact policy-and-audit wrapper for governed tool execution."""

from dataclasses import asdict, dataclass
from enum import Enum
from hashlib import sha256
import json
from typing import Any, Callable, Dict, FrozenSet, List, Mapping, Optional


class Decision(str, Enum):
    ALLOW = "allow"
    ESCALATE = "escalate"
    DENY = "deny"


@dataclass(frozen=True)
class ToolSpec:
    name: str
    consent_scope: str
    risk: str
    reversible: bool
    handler: Callable[[Mapping[str, Any]], Mapping[str, Any]]


@dataclass(frozen=True)
class PolicyContext:
    tenant_id: str
    actor_id: str
    purpose: str
    consent_scopes: FrozenSet[str]
    approved_sensitive_actions: FrozenSet[str] = frozenset()


@dataclass(frozen=True)
class ExecutionPlan:
    run_id: str
    tool_name: str
    arguments: Mapping[str, Any]
    estimated_cost_units: int
    budget_units: int


@dataclass(frozen=True)
class AuditEvent:
    run_id: str
    event: str
    decision: str
    reason: str
    evidence_hash: str


class GovernedRuntime:
    """Evaluates policy before execution and emits content-hashed audit events."""

    def __init__(self, tools: Mapping[str, ToolSpec]) -> None:
        self._tools: Dict[str, ToolSpec] = dict(tools)
        self.audit_log: List[AuditEvent] = []

    @staticmethod
    def _hash_evidence(payload: Mapping[str, Any]) -> str:
        canonical = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
        return sha256(canonical).hexdigest()

    def _record(self, plan: ExecutionPlan, event: str, decision: Decision, reason: str) -> None:
        self.audit_log.append(
            AuditEvent(
                run_id=plan.run_id,
                event=event,
                decision=decision.value,
                reason=reason,
                evidence_hash=self._hash_evidence(
                    {"plan": asdict(plan), "event": event, "decision": decision.value, "reason": reason}
                ),
            )
        )

    def evaluate(self, plan: ExecutionPlan, context: PolicyContext) -> tuple[Decision, str]:
        tool = self._tools.get(plan.tool_name)
        if tool is None:
            return Decision.DENY, "tool is not registered"
        if not context.tenant_id or not context.actor_id or not context.purpose:
            return Decision.DENY, "identity and declared purpose are required"
        if tool.consent_scope not in context.consent_scopes:
            return Decision.DENY, "required consent scope is absent"
        if plan.estimated_cost_units < 0 or plan.estimated_cost_units > plan.budget_units:
            return Decision.DENY, "plan exceeds its declared budget"
        requires_review = tool.risk in {"high", "critical"} or not tool.reversible
        if requires_review and tool.name not in context.approved_sensitive_actions:
            return Decision.ESCALATE, "sensitive action requires human approval"
        return Decision.ALLOW, "policy, consent and budget checks passed"

    def run(self, plan: ExecutionPlan, context: PolicyContext) -> Mapping[str, Any]:
        decision, reason = self.evaluate(plan, context)
        self._record(plan, "policy_evaluated", decision, reason)
        if decision is not Decision.ALLOW:
            return {"run_id": plan.run_id, "decision": decision.value, "reason": reason}

        tool = self._tools[plan.tool_name]
        result = tool.handler(plan.arguments)
        self._record(plan, "tool_completed", Decision.ALLOW, "registered tool completed")
        return {"run_id": plan.run_id, "decision": decision.value, "result": result}


def registered_tools() -> Dict[str, ToolSpec]:
    return {
        "summarize_case": ToolSpec(
            name="summarize_case",
            consent_scope="case:read",
            risk="low",
            reversible=True,
            handler=lambda args: {"summary": f"Case {args['case_id']} is ready for review."},
        ),
        "send_notice": ToolSpec(
            name="send_notice",
            consent_scope="notice:send",
            risk="high",
            reversible=False,
            handler=lambda args: {"notice_id": f"notice-{args['case_id']}"},
        ),
    }


if __name__ == "__main__":
    runtime = GovernedRuntime(registered_tools())
    plan = ExecutionPlan("run-001", "summarize_case", {"case_id": "demo-42"}, 2, 5)
    context = PolicyContext("tenant-demo", "analyst-7", "case review", frozenset({"case:read"}))
    print(json.dumps(runtime.run(plan, context), indent=2))
    print(json.dumps([asdict(event) for event in runtime.audit_log], indent=2))
