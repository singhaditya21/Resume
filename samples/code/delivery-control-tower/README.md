# Delivery control tower

A dependency-free reference implementation for deterministic portfolio health, metric lineage, material-variance detection and evidence-linked operating readouts.

## Boundary

- Deterministic functions own metric calculations and thresholds.
- Evidence records carry source, period, freshness, calculation version and owner.
- Narrative assembly can explain governed outputs but cannot create or overwrite a KPI.
- Exceptions preserve the variance, reason, action, owner and due date together.

## Run

```bash
python3 -m unittest -v
python3 control_tower.py
```

The sample uses synthetic values and generic dimensions. It contains no internal financial or client data.
