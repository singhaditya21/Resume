# Public evidence map — RMG Resource Allocation Assistant

This map connects public claim areas to anonymized samples. Original archive-member paths are intentionally not published. The source was reviewed statically and was not executed, deployed or runtime-verified.

## Evidence boundary

- Source evidence: **13 meaningful anonymized samples**
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
| System structure and runtime flow | `source/sample-01.py`, `source/sample-02.py`, `source/sample-03.py`, `source/sample-05.js`, `source/sample-11.ps1`, `source/sample-13.css` | Static code reading only |
| AI or automation role | `source/sample-01.py`, `source/sample-02.py`, `source/sample-03.py`, `source/sample-05.js`, `source/sample-06.txt`, `source/sample-09.ps1`, `source/sample-11.ps1`, `source/sample-12.html` | Static code reading only |
| Controls and validation | `source/sample-01.py`, `source/sample-04.py`, `source/sample-05.js` | Static code reading only |
| Delivery and operational seams | `source/sample-07.ps1`, `source/sample-08.py`, `source/sample-10.py` | Static code reading only |
| Documented decision evidence | Not established from the supplied archive | Static code reading only |

The map identifies evidence roles, not proof of production operation. A sample may support more than one claim area; absence of a mapped sample is shown explicitly rather than inferred.

## Published sample inventory

| Anonymized file | Evidence status | Bytes | Inferred review roles |
|---|---:|---:|---|
| `source/sample-01.py` | Meaningful sample | 7,047 | AI / retrieval, Service / API, Workflow / orchestration, Control / validation |
| `source/sample-02.py` | Meaningful sample | 7,726 | AI / retrieval, Service / API, Workflow / orchestration |
| `source/sample-03.py` | Meaningful sample | 12,290 | AI / retrieval, Service / API |
| `source/sample-04.py` | Meaningful sample | 15,857 | Test / quality, User experience |
| `source/sample-05.js` | Meaningful sample | 81,585 | AI / retrieval, Service / API, Control / validation, Test / quality |
| `source/sample-06.txt` | Meaningful sample | 203 | AI / retrieval |
| `source/sample-07.ps1` | Meaningful sample | 228 | General implementation / configuration |
| `source/sample-08.py` | Meaningful sample | 455 | General implementation / configuration |
| `source/sample-09.ps1` | Meaningful sample | 1,279 | AI / retrieval |
| `source/sample-10.py` | Meaningful sample | 2,840 | General implementation / configuration |
| `source/sample-11.ps1` | Meaningful sample | 2,995 | AI / retrieval, Service / API |
| `source/sample-12.html` | Meaningful sample | 8,416 | AI / retrieval, User experience |
| `source/sample-13.css` | Meaningful sample | 35,407 | AI / retrieval, Service / API, User experience |
