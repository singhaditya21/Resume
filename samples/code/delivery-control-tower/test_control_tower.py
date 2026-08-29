import unittest
from datetime import date, datetime, timedelta, timezone

from control_tower import EvidenceRecord, build_readout, material_variance, portfolio_health


class DeliveryControlTowerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.now = datetime(2026, 8, 29, 12, 0, tzinfo=timezone.utc)

    def test_health_is_deterministic_and_bounded(self) -> None:
        score = portfolio_health(
            {"quality": 110.0, "schedule": 80.0, "risk": 70.0},
            {"quality": 0.4, "schedule": 0.35, "risk": 0.25},
        )
        self.assertEqual(score, 85.5)

    def test_rejects_incomplete_metric_set(self) -> None:
        with self.assertRaises(ValueError):
            portfolio_health({"quality": 90.0}, {"quality": 0.5, "risk": 0.5})

    def test_materiality_suppresses_noise(self) -> None:
        self.assertIsNone(material_variance(91.0, 90.0, 3.0))
        self.assertEqual(material_variance(84.0, 90.0, 3.0), -6.0)

    def test_readout_links_variance_to_owner_and_action(self) -> None:
        record = EvidenceRecord("schedule", 74.0, "planning", "2026-W35", self.now, "v3", "Program Lead")
        readout = build_readout(
            [record],
            {"schedule": 82.0},
            {"schedule": 5.0},
            {"schedule": "critical dependency moved"},
            {"schedule": ("recover the critical path", date(2026, 9, 4))},
            self.now,
        )
        self.assertEqual(len(readout.what_changed), 1)
        self.assertIn("Program Lead", readout.actions[0])
        self.assertEqual(len(readout.evidence), 1)

    def test_stale_evidence_is_excluded(self) -> None:
        record = EvidenceRecord(
            "schedule", 74.0, "planning", "2026-W34", self.now - timedelta(hours=72), "v2", "Program Lead"
        )
        readout = build_readout([record], {"schedule": 82.0}, {"schedule": 5.0}, {}, {}, self.now)
        self.assertEqual(readout.evidence, ())
        self.assertEqual(readout.what_changed, ())


if __name__ == "__main__":
    unittest.main()
