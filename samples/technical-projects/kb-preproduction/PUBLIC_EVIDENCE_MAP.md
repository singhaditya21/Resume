# Public evidence map — AIbot RAG API — Preproduction

This map connects public claim areas to anonymized samples. Original archive-member paths are intentionally not published. The source was reviewed statically and was not executed, deployed or runtime-verified.

## Evidence boundary

- Source evidence: **19 meaningful anonymized samples**
- Retained empty placeholders: **5**
- Verification: **Static review only · code not executed**
- Delivery maturity: **Implementation archive**
- Intelligence type: **RAG / document AI**
- Ownership: **Personal ownership not established from the supplied archive.**
- Outcomes: **Measured business or runtime outcomes not established from the supplied archive.**
- Decision evidence: **Technical decision rationale not established from the supplied archive.**

## Claim-to-sample map

| Public claim area | Anonymized published evidence | Verification boundary |
|---|---|---|
| System structure and runtime flow | `source/sample-03.py`, `source/sample-04.py`, `source/sample-05.py`, `source/sample-06.txt`, `source/sample-07.txt`, `source/sample-16.py`, `source/sample-17.py`, `source/sample-18.py` | Static code reading only |
| AI or automation role | `source/sample-01.py`, `source/sample-02.py`, `source/sample-03.py`, `source/sample-04.py`, `source/sample-05.py`, `source/sample-06.txt`, `source/sample-08.txt`, `source/sample-14.py` | Static code reading only |
| Controls and validation | `source/sample-02.py`, `source/sample-03.py`, `source/sample-04.py`, `source/sample-05.py`, `source/sample-17.py`, `source/sample-21.py`, `source/sample-24.py` | Static code reading only |
| Delivery and operational seams | `source/sample-19.py`, `source/sample-23.ps1` | Static code reading only |
| Documented decision evidence | Not established from the supplied archive | Static code reading only |

The map identifies evidence roles, not proof of production operation. A sample may support more than one claim area; absence of a mapped sample is shown explicitly rather than inferred.

## Published sample inventory

| Anonymized file | Evidence status | Bytes | Inferred review roles |
|---|---:|---:|---|
| `source/sample-01.py` | Meaningful sample | 117 | AI / retrieval |
| `source/sample-02.py` | Meaningful sample | 287 | AI / retrieval, Control / validation |
| `source/sample-03.py` | Meaningful sample | 1,601 | AI / retrieval, Service / API, Data / persistence, Control / validation |
| `source/sample-04.py` | Meaningful sample | 2,136 | AI / retrieval, Service / API, Control / validation |
| `source/sample-05.py` | Meaningful sample | 3,362 | AI / retrieval, Data / persistence, Control / validation |
| `source/sample-06.txt` | Meaningful sample | 156 | AI / retrieval, Data / persistence |
| `source/sample-07.txt` | Meaningful sample | 250 | Service / API |
| `source/sample-08.txt` | Meaningful sample | 463 | AI / retrieval |
| `source/sample-09.py` | Retained empty placeholder | 0 | General implementation / configuration |
| `source/sample-10.py` | Retained empty placeholder | 0 | General implementation / configuration |
| `source/sample-11.py` | Retained empty placeholder | 0 | General implementation / configuration |
| `source/sample-12.py` | Retained empty placeholder | 0 | General implementation / configuration |
| `source/sample-13.py` | Retained empty placeholder | 0 | General implementation / configuration |
| `source/sample-14.py` | Meaningful sample | 70 | AI / retrieval |
| `source/sample-15.py` | Meaningful sample | 120 | AI / retrieval |
| `source/sample-16.py` | Meaningful sample | 187 | Service / API |
| `source/sample-17.py` | Meaningful sample | 626 | Data / persistence, Control / validation |
| `source/sample-18.py` | Meaningful sample | 710 | AI / retrieval, Data / persistence |
| `source/sample-19.py` | Meaningful sample | 864 | General implementation / configuration |
| `source/sample-20.py` | Meaningful sample | 868 | Service / API |
| `source/sample-21.py` | Meaningful sample | 970 | Control / validation |
| `source/sample-22.sh` | Meaningful sample | 1,579 | AI / retrieval, Service / API |
| `source/sample-23.ps1` | Meaningful sample | 1,590 | General implementation / configuration |
| `source/sample-24.py` | Meaningful sample | 2,155 | Data / persistence, Control / validation |
