"""Deterministic portfolio metrics and evidence-linked operating narration."""

from dataclasses import asdict, dataclass
from datetime import date, datetime, timezone
import json
from typing import Iterable, List, Mapping, Optional, Tuple


@dataclass(frozen=True)
class EvidenceRecord:
    metric: str
    value: float
    source: str
    period: str
    calculated_at: datetime
    calculation_version: str
    owner: str


@dataclass(frozen=True)
class ExceptionRecord:
    metric: str
    variance: float
    threshold: float
    reason: str
    owner: str
    due_date: date


@dataclass(frozen=True)
class OperatingReadout:
    what_changed: Tuple[str, ...]
    why_it_changed: Tuple[str, ...]
    actions: Tuple[str, ...]
    evidence: Tuple[EvidenceRecord, ...]


def validate_weights(weights: Mapping[str, float]) -> None:
    if not weights or any(weight < 0 for weight in weights.values()):
        raise ValueError("weights must be non-negative")
    if abs(sum(weights.values()) - 1.0) > 1e-9:
        raise ValueError("weights must sum to 1.0")


def portfolio_health(metrics: Mapping[str, float], weights: Mapping[str, float]) -> float:
    validate_weights(weights)
    missing = set(weights).difference(metrics)
    if missing:
        raise ValueError(f"missing governed metrics: {sorted(missing)}")
    bounded = {name: min(100.0, max(0.0, metrics[name])) for name in weights}
    return round(sum(bounded[name] * weights[name] for name in weights), 2)


def material_variance(current: float, baseline: float, threshold: float) -> Optional[float]:
    if threshold < 0:
        raise ValueError("threshold must be non-negative")
    variance = round(current - baseline, 2)
    return variance if abs(variance) >= threshold else None


def stale(record: EvidenceRecord, now: datetime, max_age_hours: int) -> bool:
    age = now - record.calculated_at
    return age.total_seconds() > max_age_hours * 3600


def build_readout(
    evidence: Iterable[EvidenceRecord],
    baselines: Mapping[str, float],
    thresholds: Mapping[str, float],
    explanations: Mapping[str, str],
    actions: Mapping[str, tuple[str, date]],
    now: datetime,
    max_age_hours: int = 48,
) -> OperatingReadout:
    valid: List[EvidenceRecord] = []
    changed: List[str] = []
    reasons: List[str] = []
    next_actions: List[str] = []

    for record in evidence:
        if stale(record, now, max_age_hours):
            continue
        if not record.source or not record.period or not record.calculation_version or not record.owner:
            raise ValueError(f"incomplete lineage for {record.metric}")
        valid.append(record)
        variance = material_variance(
            record.value,
            baselines.get(record.metric, record.value),
            thresholds.get(record.metric, float("inf")),
        )
        if variance is None:
            continue
        changed.append(f"{record.metric} changed by {variance:+.2f} against baseline")
        reasons.append(f"{record.metric}: {explanations.get(record.metric, 'driver requires owner validation')}")
        action, due = actions.get(record.metric, ("confirm recovery action", now.date()))
        next_actions.append(f"{record.owner}: {action} by {due.isoformat()}")

    return OperatingReadout(tuple(changed), tuple(reasons), tuple(next_actions), tuple(valid))


if __name__ == "__main__":
    now = datetime.now(timezone.utc)
    records = [
        EvidenceRecord("quality", 91.0, "delivery_service", "2026-W35", now, "v2", "Quality Lead"),
        EvidenceRecord("schedule", 74.0, "planning_service", "2026-W35", now, "v3", "Program Lead"),
    ]
    readout = build_readout(
        records,
        baselines={"quality": 90.0, "schedule": 82.0},
        thresholds={"quality": 3.0, "schedule": 5.0},
        explanations={"schedule": "two critical dependencies moved beyond their committed dates"},
        actions={"schedule": ("recover the critical path and re-baseline", date(2026, 9, 4))},
        now=now,
    )
    print(json.dumps(asdict(readout), indent=2, default=str))
