# Governed agent runtime

A dependency-free reference implementation of the control path used around an enterprise agent: registered tools, consent scopes, risk policy, bounded budgets, human approval and content-hashed audit records.

## Decision flow

1. Validate that the requested tool is registered.
2. Confirm tenant, purpose and consent scope.
3. Check plan cost against the declared run budget.
4. Escalate sensitive or irreversible actions for human approval.
5. Execute only after an `ALLOW` decision and record every state transition.

## Run

```bash
python3 -m unittest -v
python3 runtime.py
```

This is a sanitized reference implementation. It contains no client code or deployment configuration.
