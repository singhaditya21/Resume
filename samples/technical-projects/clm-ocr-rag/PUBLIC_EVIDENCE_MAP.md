# Public evidence map — Contract OCR & Local RAG

This map connects public claim areas to anonymized samples. Original archive-member paths are intentionally not published. The source was reviewed statically and was not executed, deployed or runtime-verified.

## Evidence boundary

- Source evidence: **24 meaningful anonymized samples**
- Retained empty placeholders: **0**
- Verification: **Static review only · code not executed**
- Delivery maturity: **Implementation archive**
- Intelligence type: **RAG / document AI**
- Ownership: **Personal ownership not established from the supplied archive.**
- Outcomes: **Measured business or runtime outcomes not established from the supplied archive.**
- Decision evidence: **The inference boundary stays local while dense and lexical retrieval are combined before reranking. Answer citations remain tied to retrieved chunks rather than model-only assertions.**

## Claim-to-sample map

| Public claim area | Anonymized published evidence | Verification boundary |
|---|---|---|
| System structure and runtime flow | `source/sample-01.py`, `source/sample-02.py`, `source/sample-03.py`, `source/sample-04.py`, `source/sample-05.py`, `source/sample-06.py`, `source/sample-07.txt`, `source/sample-08.txt` | Static code reading only |
| AI or automation role | `source/sample-01.py`, `source/sample-02.py`, `source/sample-03.py`, `source/sample-04.py`, `source/sample-05.py`, `source/sample-06.py`, `source/sample-08.txt`, `source/sample-10.py` | Static code reading only |
| Controls and validation | `source/sample-05.py`, `source/sample-06.py`, `source/sample-20.py` | Static code reading only |
| Delivery and operational seams | `source/sample-09.py`, `source/sample-11.py`, `source/sample-17.py` | Static code reading only |
| Documented decision evidence | `source/sample-02.py`, `source/sample-03.py`, `source/sample-05.py`, `source/sample-06.py`, `source/sample-07.txt`, `source/sample-08.txt`, `source/sample-16.py`, `source/sample-20.py` | Static code reading only |

The map identifies evidence roles, not proof of production operation. A sample may support more than one claim area; absence of a mapped sample is shown explicitly rather than inferred.

## Published sample inventory

| Anonymized file | Evidence status | Bytes | Inferred review roles |
|---|---:|---:|---|
| `source/sample-01.py` | Meaningful sample | 1,876 | AI / retrieval, Service / API |
| `source/sample-02.py` | Meaningful sample | 4,743 | Workflow / orchestration, User experience |
| `source/sample-03.py` | Meaningful sample | 5,012 | AI / retrieval, Service / API, Workflow / orchestration, Data / persistence |
| `source/sample-04.py` | Meaningful sample | 5,187 | AI / retrieval, Service / API |
| `source/sample-05.py` | Meaningful sample | 6,872 | AI / retrieval, Data / persistence, Control / validation |
| `source/sample-06.py` | Meaningful sample | 25,220 | AI / retrieval, Service / API, Data / persistence, Control / validation |
| `source/sample-07.txt` | Meaningful sample | 232 | Service / API, Data / persistence |
| `source/sample-08.txt` | Meaningful sample | 1,685 | AI / retrieval, Data / persistence |
| `source/sample-09.py` | Meaningful sample | 13 | General implementation / configuration |
| `source/sample-10.py` | Meaningful sample | 13 | AI / retrieval |
| `source/sample-11.py` | Meaningful sample | 16 | General implementation / configuration |
| `source/sample-12.py` | Meaningful sample | 19 | AI / retrieval |
| `source/sample-13.py` | Meaningful sample | 19 | AI / retrieval |
| `source/sample-14.py` | Meaningful sample | 576 | AI / retrieval |
| `source/sample-15.ps1` | Meaningful sample | 931 | AI / retrieval, Service / API |
| `source/sample-16.py` | Meaningful sample | 955 | AI / retrieval, Data / persistence |
| `source/sample-17.py` | Meaningful sample | 993 | General implementation / configuration |
| `source/sample-18.py` | Meaningful sample | 1,068 | AI / retrieval, Service / API |
| `source/sample-19.py` | Meaningful sample | 1,069 | AI / retrieval |
| `source/sample-20.py` | Meaningful sample | 1,227 | AI / retrieval, Control / validation |
| `source/sample-21.py` | Meaningful sample | 1,313 | AI / retrieval, Service / API, Workflow / orchestration |
| `source/sample-22.py` | Meaningful sample | 1,567 | User experience |
| `source/sample-23.ps1` | Meaningful sample | 2,006 | Service / API |
| `source/sample-24.py` | Meaningful sample | 2,090 | AI / retrieval |
