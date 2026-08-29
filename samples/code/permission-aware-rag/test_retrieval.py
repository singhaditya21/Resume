import unittest

from retrieval import Document, Evidence, ResponseMode, decide_response, retrieve


class PermissionAwareRetrievalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.documents = [
            Document("a", "Approval evidence for a sensitive action.", frozenset({"risk"}), 0.9),
            Document("b", "Evidence events retain the decision owner.", frozenset({"risk", "ops"}), 0.8),
            Document("c", "Private finance evidence.", frozenset({"finance"}), 0.99),
        ]

    def test_filters_acl_before_ranking(self) -> None:
        result = retrieve("finance evidence", self.documents, frozenset({"risk"}), min_evidence=1)
        ids = {item.document_id for item in result.evidence}
        self.assertNotIn("c", ids)

    def test_answers_with_permitted_coverage(self) -> None:
        result = retrieve("approval evidence owner", self.documents, frozenset({"risk"}))
        self.assertEqual(result.mode, ResponseMode.ANSWER)
        self.assertEqual(len(result.evidence), 2)

    def test_clarifies_when_coverage_is_narrow(self) -> None:
        result = retrieve("approval", self.documents[:1], frozenset({"risk"}), min_evidence=2)
        self.assertEqual(result.mode, ResponseMode.CLARIFY)

    def test_refuses_without_permitted_evidence(self) -> None:
        result = retrieve("finance", self.documents, frozenset({"guest"}), min_evidence=1)
        self.assertEqual(result.mode, ResponseMode.REFUSE)

    def test_refuses_low_confidence(self) -> None:
        weak_evidence = (Evidence("a", "weakly related evidence", 0.1),)
        mode, _ = decide_response(weak_evidence, min_score=0.5, min_evidence=1)
        self.assertEqual(mode, ResponseMode.REFUSE)


if __name__ == "__main__":
    unittest.main()
