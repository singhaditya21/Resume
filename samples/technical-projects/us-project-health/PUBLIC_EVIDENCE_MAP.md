# Public evidence map — US Project Health Dashboard

This map connects public claim areas to anonymized samples. Original archive-member paths are intentionally not published. The source was reviewed statically and was not executed, deployed or runtime-verified.

## Evidence boundary

- Source evidence: **14 meaningful anonymized samples**
- Retained empty placeholders: **0**
- Verification: **Static review only · code not executed**
- Delivery maturity: **Deterministic implementation archive**
- Intelligence type: **Deterministic / AI-enabling**
- Ownership: **Personal ownership not established from the supplied archive.**
- Outcomes: **Measured business or runtime outcomes not established from the supplied archive.**
- Decision evidence: **Technical decision rationale not established from the supplied archive.**

## Claim-to-sample map

| Public claim area | Anonymized published evidence | Verification boundary |
|---|---|---|
| System structure and runtime flow | `source/sample-01.py`, `source/sample-03.py`, `source/sample-04.py`, `source/sample-05.py`, `source/sample-06.txt`, `source/sample-12.py`, `source/sample-14.html` | Static code reading only |
| AI or automation role | `source/sample-02.py`, `source/sample-03.py`, `source/sample-05.py`, `source/sample-12.py`, `source/sample-14.html` | Static code reading only |
| Controls and validation | `source/sample-03.py`, `source/sample-04.py`, `source/sample-05.py` | Static code reading only |
| Delivery and operational seams | `source/sample-04.py`, `source/sample-07.txt`, `source/sample-08.py`, `source/sample-09.py`, `source/sample-11.py` | Static code reading only |
| Documented decision evidence | Not established from the supplied archive | Static code reading only |

The map identifies evidence roles, not proof of production operation. A sample may support more than one claim area; absence of a mapped sample is shown explicitly rather than inferred.

## Published sample inventory

| Anonymized file | Evidence status | Bytes | Inferred review roles |
|---|---:|---:|---|
| `source/sample-01.py` | Meaningful sample | 3,912 | Service / API |
| `source/sample-02.py` | Meaningful sample | 4,159 | AI / retrieval, User experience |
| `source/sample-03.py` | Meaningful sample | 10,406 | AI / retrieval, Service / API, Control / validation |
| `source/sample-04.py` | Meaningful sample | 19,051 | Service / API, Control / validation, User experience, Operations / delivery |
| `source/sample-05.py` | Meaningful sample | 29,483 | AI / retrieval, Service / API, Data / persistence, Control / validation |
| `source/sample-06.txt` | Meaningful sample | 63 | Service / API |
| `source/sample-07.txt` | Meaningful sample | 217 | General implementation / configuration |
| `source/sample-08.py` | Meaningful sample | 480 | General implementation / configuration |
| `source/sample-09.py` | Meaningful sample | 1,626 | Operations / delivery |
| `source/sample-10.html` | Meaningful sample | 2,925 | User experience |
| `source/sample-11.py` | Meaningful sample | 4,243 | General implementation / configuration |
| `source/sample-12.py` | Meaningful sample | 11,554 | AI / retrieval, Service / API |
| `source/sample-13.html` | Meaningful sample | 25,772 | User experience |
| `source/sample-14.html` | Meaningful sample | 78,864 | AI / retrieval, Service / API, User experience |
