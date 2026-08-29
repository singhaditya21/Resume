# Permission-aware RAG

A dependency-free reference of an ACL-first retrieval path. Authorization constrains the candidate set before lexical and semantic ranking; reciprocal-rank fusion combines signals; a response policy selects `ANSWER`, `CLARIFY` or `REFUSE`.

## Design principles

- Permission is evaluated before relevance.
- Lexical and semantic signals remain independently inspectable.
- Citations stay attached to ranked evidence.
- Low coverage, weak confidence or policy failure changes the response mode.

## Run

```bash
python3 -m unittest -v
python3 retrieval.py
```

This is a sanitized teaching implementation, not client source code or a production vector-store adapter.
