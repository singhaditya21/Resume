# Public evidence map — CRM Data Audit Framework

This map connects public claim areas to anonymized samples. Original archive-member paths are intentionally not published. The source was reviewed statically and was not executed, deployed or runtime-verified.

## Evidence boundary

- Source evidence: **24 meaningful anonymized samples**
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
| System structure and runtime flow | `source/sample-01.js`, `source/sample-03.js`, `source/sample-04.js`, `source/sample-05.js`, `source/sample-08.json`, `source/sample-11.js`, `source/sample-14.js`, `source/sample-16.tsx` | Static code reading only |
| AI or automation role | `source/sample-03.js`, `source/sample-08.json`, `source/sample-11.js` | Static code reading only |
| Controls and validation | `source/sample-01.js`, `source/sample-02.tsx`, `source/sample-03.js`, `source/sample-04.js`, `source/sample-05.js`, `source/sample-10.js`, `source/sample-12.ts`, `source/sample-13.js` | Static code reading only |
| Delivery and operational seams | `source/sample-06.txt` | Static code reading only |
| Documented decision evidence | Not established from the supplied archive | Static code reading only |

The map identifies evidence roles, not proof of production operation. A sample may support more than one claim area; absence of a mapped sample is shown explicitly rather than inferred.

## Published sample inventory

| Anonymized file | Evidence status | Bytes | Inferred review roles |
|---|---:|---:|---|
| `source/sample-01.js` | Meaningful sample | 963 | Data / persistence, Control / validation |
| `source/sample-02.tsx` | Meaningful sample | 5,613 | Control / validation, User experience |
| `source/sample-03.js` | Meaningful sample | 6,592 | Service / API, Workflow / orchestration, Data / persistence, Control / validation |
| `source/sample-04.js` | Meaningful sample | 7,308 | Data / persistence, Control / validation |
| `source/sample-05.js` | Meaningful sample | 8,803 | Service / API, Data / persistence, Control / validation |
| `source/sample-06.txt` | Meaningful sample | 95 | General implementation / configuration |
| `source/sample-07.json` | Meaningful sample | 596 | User experience |
| `source/sample-08.json` | Meaningful sample | 624 | Workflow / orchestration, User experience |
| `source/sample-09.tsx` | Meaningful sample | 237 | User experience |
| `source/sample-10.js` | Meaningful sample | 834 | Control / validation |
| `source/sample-11.js` | Meaningful sample | 870 | Workflow / orchestration |
| `source/sample-12.ts` | Meaningful sample | 884 | Control / validation |
| `source/sample-13.js` | Meaningful sample | 990 | Control / validation |
| `source/sample-14.js` | Meaningful sample | 1,117 | Data / persistence, Control / validation |
| `source/sample-15.ts` | Meaningful sample | 1,294 | Control / validation |
| `source/sample-16.tsx` | Meaningful sample | 1,608 | Data / persistence, Control / validation, User experience |
| `source/sample-17.js` | Meaningful sample | 1,884 | Data / persistence, Control / validation |
| `source/sample-18.css` | Meaningful sample | 1,930 | User experience |
| `source/sample-19.js` | Meaningful sample | 3,009 | Data / persistence, Control / validation, User experience |
| `source/sample-20.tsx` | Meaningful sample | 3,358 | User experience |
| `source/sample-21.tsx` | Meaningful sample | 4,042 | Service / API, Data / persistence, Control / validation, User experience |
| `source/sample-22.tsx` | Meaningful sample | 4,449 | User experience |
| `source/sample-23.tsx` | Meaningful sample | 4,738 | Control / validation, User experience |
| `source/sample-24.tsx` | Meaningful sample | 6,776 | Service / API, Data / persistence, User experience |
