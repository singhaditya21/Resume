# Public evidence map — Zeno RAG Ingestion Platform

This map connects public claim areas to anonymized samples. Original archive-member paths are intentionally not published. The source was reviewed statically and was not executed, deployed or runtime-verified.

## Evidence boundary

- Source evidence: **15 meaningful anonymized samples**
- Retained empty placeholders: **9**
- Verification: **Static review only · code not executed**
- Delivery maturity: **Implementation archive**
- Intelligence type: **RAG / document AI**
- Ownership: **Personal ownership not established from the supplied archive.**
- Outcomes: **Measured business or runtime outcomes not established from the supplied archive.**
- Decision evidence: **ACL metadata is preserved through ingestion and vector persistence. Embedding contracts, delete guards and a recovery ledger bound repeatable ingestion.**

## Claim-to-sample map

| Public claim area | Anonymized published evidence | Verification boundary |
|---|---|---|
| System structure and runtime flow | `source/sample-01.py`, `source/sample-02.py`, `source/sample-03.py`, `source/sample-04.py`, `source/sample-05.txt`, `source/sample-06.txt`, `source/sample-07.toml`, `source/sample-08.txt` | Static code reading only |
| AI or automation role | `source/sample-01.py`, `source/sample-02.py`, `source/sample-03.py`, `source/sample-04.py`, `source/sample-06.txt`, `source/sample-07.toml`, `source/sample-08.txt`, `source/sample-09.txt` | Static code reading only |
| Controls and validation | `source/sample-02.py`, `source/sample-03.py`, `source/sample-05.txt`, `source/sample-06.txt`, `source/sample-07.toml`, `source/sample-09.txt`, `source/sample-21.py` | Static code reading only |
| Delivery and operational seams | `source/sample-05.txt`, `source/sample-08.txt`, `source/sample-19.yaml`, `source/sample-20.yaml`, `source/sample-22.yaml`, `source/sample-24.yml` | Static code reading only |
| Documented decision evidence | `source/sample-01.py`, `source/sample-02.py`, `source/sample-03.py`, `source/sample-04.py`, `source/sample-05.txt`, `source/sample-06.txt`, `source/sample-07.toml`, `source/sample-08.txt` | Static code reading only |

The map identifies evidence roles, not proof of production operation. A sample may support more than one claim area; absence of a mapped sample is shown explicitly rather than inferred.

## Published sample inventory

| Anonymized file | Evidence status | Bytes | Inferred review roles |
|---|---:|---:|---|
| `source/sample-01.py` | Meaningful sample | 5,684 | AI / retrieval, Service / API, Workflow / orchestration, Data / persistence |
| `source/sample-02.py` | Meaningful sample | 16,320 | AI / retrieval, Service / API, Data / persistence, Control / validation |
| `source/sample-03.py` | Meaningful sample | 19,120 | AI / retrieval, Service / API, Workflow / orchestration, Control / validation |
| `source/sample-04.py` | Meaningful sample | 28,320 | AI / retrieval, Service / API, Workflow / orchestration, Data / persistence |
| `source/sample-05.txt` | Meaningful sample | 1,565 | Data / persistence, Test / quality, Operations / delivery |
| `source/sample-06.txt` | Meaningful sample | 2,290 | AI / retrieval, Service / API, Data / persistence, Control / validation |
| `source/sample-07.toml` | Meaningful sample | 2,611 | AI / retrieval, Service / API, Data / persistence, Control / validation |
| `source/sample-08.txt` | Meaningful sample | 2,804 | Service / API, Workflow / orchestration, Operations / delivery |
| `source/sample-09.txt` | Meaningful sample | 10,175 | Service / API, Workflow / orchestration, Data / persistence, Control / validation |
| `source/sample-10.py` | Retained empty placeholder | 0 | General implementation / configuration |
| `source/sample-11.py` | Retained empty placeholder | 0 | General implementation / configuration |
| `source/sample-12.py` | Retained empty placeholder | 0 | General implementation / configuration |
| `source/sample-13.py` | Retained empty placeholder | 0 | General implementation / configuration |
| `source/sample-14.py` | Retained empty placeholder | 0 | General implementation / configuration |
| `source/sample-15.py` | Retained empty placeholder | 0 | General implementation / configuration |
| `source/sample-16.py` | Retained empty placeholder | 0 | General implementation / configuration |
| `source/sample-17.py` | Retained empty placeholder | 0 | General implementation / configuration |
| `source/sample-18.py` | Retained empty placeholder | 0 | General implementation / configuration |
| `source/sample-19.yaml` | Meaningful sample | 187 | Service / API, Configuration / infrastructure |
| `source/sample-20.yaml` | Meaningful sample | 622 | Service / API, Configuration / infrastructure |
| `source/sample-21.py` | Meaningful sample | 923 | Service / API, Workflow / orchestration, Control / validation |
| `source/sample-22.yaml` | Meaningful sample | 1,227 | Service / API, Data / persistence, Operations / delivery, Configuration / infrastructure |
| `source/sample-23.py` | Meaningful sample | 2,111 | AI / retrieval |
| `source/sample-24.yml` | Meaningful sample | 2,324 | Service / API, Data / persistence, Operations / delivery, Configuration / infrastructure |
