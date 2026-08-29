import unittest

from runtime import Decision, ExecutionPlan, GovernedRuntime, PolicyContext, registered_tools


class GovernedRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.runtime = GovernedRuntime(registered_tools())
        self.context = PolicyContext("tenant", "actor", "case review", frozenset({"case:read"}))

    def test_allows_registered_bounded_read(self) -> None:
        plan = ExecutionPlan("r1", "summarize_case", {"case_id": "42"}, 2, 5)
        result = self.runtime.run(plan, self.context)
        self.assertEqual(result["decision"], Decision.ALLOW.value)
        self.assertEqual(len(self.runtime.audit_log), 2)

    def test_denies_unregistered_tool(self) -> None:
        plan = ExecutionPlan("r2", "unknown", {}, 1, 5)
        decision, reason = self.runtime.evaluate(plan, self.context)
        self.assertEqual(decision, Decision.DENY)
        self.assertIn("registered", reason)

    def test_denies_missing_consent(self) -> None:
        plan = ExecutionPlan("r3", "send_notice", {"case_id": "42"}, 1, 5)
        decision, _ = self.runtime.evaluate(plan, self.context)
        self.assertEqual(decision, Decision.DENY)

    def test_denies_budget_overrun(self) -> None:
        plan = ExecutionPlan("r4", "summarize_case", {"case_id": "42"}, 6, 5)
        decision, _ = self.runtime.evaluate(plan, self.context)
        self.assertEqual(decision, Decision.DENY)

    def test_escalates_irreversible_action_until_approved(self) -> None:
        plan = ExecutionPlan("r5", "send_notice", {"case_id": "42"}, 1, 5)
        context = PolicyContext("tenant", "actor", "notice", frozenset({"notice:send"}))
        self.assertEqual(self.runtime.evaluate(plan, context)[0], Decision.ESCALATE)
        approved = PolicyContext(
            "tenant", "actor", "notice", frozenset({"notice:send"}), frozenset({"send_notice"})
        )
        self.assertEqual(self.runtime.evaluate(plan, approved)[0], Decision.ALLOW)


if __name__ == "__main__":
    unittest.main()
