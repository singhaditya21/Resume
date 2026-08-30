# Public evidence map — AIbot Production RAG API

This map connects public claim areas to anonymized samples. Original archive-member paths are intentionally not published. The source was reviewed statically and was not executed, deployed or runtime-verified.

## Evidence boundary

- Source evidence: **24 meaningful anonymized samples**
- Retained empty placeholders: **0**
- Verification: **Static review only · code not executed**
- Delivery maturity: **Prototype archive**
- Intelligence type: **RAG / document AI**
- Ownership: **Personal ownership not established from the supplied archive.**
- Outcomes: **Measured business or runtime outcomes not established from the supplied archive.**
- Decision evidence: **Technical decision rationale not established from the supplied archive.**

## Claim-to-sample map

| Public claim area | Anonymized published evidence | Verification boundary |
|---|---|---|
| System structure and runtime flow | `source/sample-02.py`, `source/sample-03.py`, `source/sample-07.txt`, `source/sample-08.py`, `source/sample-09.py`, `source/sample-10.py`, `source/sample-18.py`, `source/sample-19.py` | Static code reading only |
| AI or automation role | `source/sample-01.py`, `source/sample-02.py`, `source/sample-03.py`, `source/sample-12.py`, `source/sample-14.py`, `source/sample-16.py`, `source/sample-17.py`, `source/sample-19.py` | Static code reading only |
| Controls and validation | `source/sample-01.py`, `source/sample-02.py`, `source/sample-03.py`, `source/sample-04.txt`, `source/sample-05.txt`, `source/sample-20.py` | Static code reading only |
| Delivery and operational seams | `source/sample-06.txt`, `source/sample-11.py`, `source/sample-13.py`, `source/sample-15.py`, `source/sample-22.py` | Static code reading only |
| Documented decision evidence | Not established from the supplied archive | Static code reading only |

The map identifies evidence roles, not proof of production operation. A sample may support more than one claim area; absence of a mapped sample is shown explicitly rather than inferred.

## Published sample inventory

| Anonymized file | Evidence status | Bytes | Inferred review roles |
|---|---:|---:|---|
| `source/sample-01.py` | Meaningful sample | 288 | AI / retrieval, Control / validation |
| `source/sample-02.py` | Meaningful sample | 1,602 | AI / retrieval, Service / API, Data / persistence, Control / validation |
| `source/sample-03.py` | Meaningful sample | 2,034 | AI / retrieval, Service / API, Control / validation |
| `source/sample-04.txt` | Meaningful sample | 48 | Test / quality |
| `source/sample-05.txt` | Meaningful sample | 62 | Test / quality |
| `source/sample-06.txt` | Meaningful sample | 204 | General implementation / configuration |
| `source/sample-07.txt` | Meaningful sample | 221 | Service / API |
| `source/sample-08.py` | Meaningful sample | 19 | Data / persistence |
| `source/sample-09.py` | Meaningful sample | 25 | Service / API |
| `source/sample-10.py` | Meaningful sample | 25 | Service / API |
| `source/sample-11.py` | Meaningful sample | 29 | General implementation / configuration |
| `source/sample-12.py` | Meaningful sample | 37 | AI / retrieval |
| `source/sample-13.py` | Meaningful sample | 42 | General implementation / configuration |
| `source/sample-14.py` | Meaningful sample | 42 | AI / retrieval |
| `source/sample-15.py` | Meaningful sample | 72 | General implementation / configuration |
| `source/sample-16.py` | Meaningful sample | 118 | AI / retrieval |
| `source/sample-17.py` | Meaningful sample | 121 | AI / retrieval |
| `source/sample-18.py` | Meaningful sample | 188 | Service / API |
| `source/sample-19.py` | Meaningful sample | 636 | AI / retrieval, Service / API, Data / persistence |
| `source/sample-20.py` | Meaningful sample | 736 | Control / validation |
| `source/sample-21.py` | Meaningful sample | 869 | Service / API |
| `source/sample-22.py` | Meaningful sample | 1,023 | General implementation / configuration |
| `source/sample-23.py` | Meaningful sample | 1,079 | AI / retrieval, Service / API, Data / persistence |
| `source/sample-24.py` | Meaningful sample | 2,109 | Service / API |
