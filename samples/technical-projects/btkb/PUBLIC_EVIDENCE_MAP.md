# Public evidence map — Zeno Enterprise Knowledge Assistant

This map connects public claim areas to anonymized samples. Original archive-member paths are intentionally not published. The source was reviewed statically and was not executed, deployed or runtime-verified.

## Evidence boundary

- Source evidence: **24 meaningful anonymized samples**
- Retained empty placeholders: **0**
- Verification: **Static review only · code not executed**
- Delivery maturity: **Implementation archive**
- Intelligence type: **RAG / document AI**
- Ownership: **Personal ownership not established from the supplied archive.**
- Outcomes: **Measured business or runtime outcomes not established from the supplied archive.**
- Decision evidence: **ACL checks occur before generation, with confidence-based refusal when evidence is insufficient. Generated output passes through credential scrubbing before delivery.**

## Claim-to-sample map

| Public claim area | Anonymized published evidence | Verification boundary |
|---|---|---|
| System structure and runtime flow | `source/sample-02.py`, `source/sample-03.py`, `source/sample-04.py`, `source/sample-05.py`, `source/sample-08.txt`, `source/sample-09.txt`, `source/sample-10.txt`, `source/sample-11.py` | Static code reading only |
| AI or automation role | `source/sample-01.py`, `source/sample-02.py`, `source/sample-03.py`, `source/sample-04.py`, `source/sample-05.py`, `source/sample-09.txt`, `source/sample-10.txt`, `source/sample-12.py` | Static code reading only |
| Controls and validation | `source/sample-02.py`, `source/sample-03.py`, `source/sample-04.py`, `source/sample-07.json`, `source/sample-08.txt`, `source/sample-09.txt`, `source/sample-20.yaml`, `source/sample-23.yaml` | Static code reading only |
| Delivery and operational seams | `source/sample-06.txt`, `source/sample-08.txt`, `source/sample-15.yaml`, `source/sample-16.js`, `source/sample-17.yaml`, `source/sample-18.js`, `source/sample-20.yaml`, `source/sample-22.js` | Static code reading only |
| Documented decision evidence | `source/sample-02.py`, `source/sample-03.py`, `source/sample-04.py`, `source/sample-05.py`, `source/sample-07.json`, `source/sample-08.txt`, `source/sample-09.txt`, `source/sample-10.txt` | Static code reading only |

The map identifies evidence roles, not proof of production operation. A sample may support more than one claim area; absence of a mapped sample is shown explicitly rather than inferred.

## Published sample inventory

| Anonymized file | Evidence status | Bytes | Inferred review roles |
|---|---:|---:|---|
| `source/sample-01.py` | Meaningful sample | 7,244 | AI / retrieval |
| `source/sample-02.py` | Meaningful sample | 9,580 | AI / retrieval, Service / API, Control / validation |
| `source/sample-03.py` | Meaningful sample | 10,674 | AI / retrieval, Service / API, Data / persistence, Control / validation |
| `source/sample-04.py` | Meaningful sample | 12,536 | AI / retrieval, Service / API, Workflow / orchestration, Control / validation |
| `source/sample-05.py` | Meaningful sample | 118,186 | AI / retrieval, Service / API, Workflow / orchestration, Data / persistence |
| `source/sample-06.txt` | Meaningful sample | 112 | General implementation / configuration |
| `source/sample-07.json` | Meaningful sample | 739 | Control / validation, User experience |
| `source/sample-08.txt` | Meaningful sample | 1,092 | Data / persistence, Test / quality, Operations / delivery |
| `source/sample-09.txt` | Meaningful sample | 1,806 | AI / retrieval, Service / API, Data / persistence, Test / quality |
| `source/sample-10.txt` | Meaningful sample | 6,202 | AI / retrieval, Service / API, Workflow / orchestration, Data / persistence |
| `source/sample-11.py` | Meaningful sample | 25 | Service / API |
| `source/sample-12.py` | Meaningful sample | 27 | AI / retrieval |
| `source/sample-13.py` | Meaningful sample | 74 | AI / retrieval, Service / API |
| `source/sample-14.py` | Meaningful sample | 77 | AI / retrieval |
| `source/sample-15.yaml` | Meaningful sample | 100 | Operations / delivery, Configuration / infrastructure |
| `source/sample-16.js` | Meaningful sample | 138 | General implementation / configuration |
| `source/sample-17.yaml` | Meaningful sample | 228 | Service / API, User experience, Operations / delivery, Configuration / infrastructure |
| `source/sample-18.js` | Meaningful sample | 249 | General implementation / configuration |
| `source/sample-19.js` | Meaningful sample | 255 | Service / API, User experience |
| `source/sample-20.yaml` | Meaningful sample | 394 | Service / API, Control / validation, Configuration / infrastructure |
| `source/sample-21.js` | Meaningful sample | 532 | Service / API, User experience |
| `source/sample-22.js` | Meaningful sample | 644 | General implementation / configuration |
| `source/sample-23.yaml` | Meaningful sample | 679 | Data / persistence, Control / validation, Operations / delivery, Configuration / infrastructure |
| `source/sample-24.yaml` | Meaningful sample | 777 | Service / API, Operations / delivery, Configuration / infrastructure |
