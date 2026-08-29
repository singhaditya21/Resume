"""ACL-first hybrid retrieval with explicit response-mode policy."""

from dataclasses import asdict, dataclass
from enum import Enum
import json
import math
import re
from typing import Dict, FrozenSet, Iterable, List, Sequence, Tuple


TOKEN_PATTERN = re.compile(r"[a-z0-9]+")


class ResponseMode(str, Enum):
    ANSWER = "answer"
    CLARIFY = "clarify"
    REFUSE = "refuse"


@dataclass(frozen=True)
class Document:
    document_id: str
    text: str
    acl: FrozenSet[str]
    semantic_score: float


@dataclass(frozen=True)
class Evidence:
    document_id: str
    excerpt: str
    score: float


@dataclass(frozen=True)
class RetrievalResult:
    mode: ResponseMode
    reason: str
    evidence: Tuple[Evidence, ...]


def tokenize(text: str) -> List[str]:
    return TOKEN_PATTERN.findall(text.lower())


def permitted(document: Document, principals: FrozenSet[str]) -> bool:
    return bool(document.acl.intersection(principals))


def lexical_score(query: str, document: Document) -> float:
    query_tokens = tokenize(query)
    document_tokens = tokenize(document.text)
    if not query_tokens or not document_tokens:
        return 0.0
    counts: Dict[str, int] = {}
    for token in document_tokens:
        counts[token] = counts.get(token, 0) + 1
    matched = sum(1.0 + math.log(counts.get(token, 1)) for token in set(query_tokens) if token in counts)
    return matched / math.sqrt(len(document_tokens))


def ranked_ids(items: Iterable[tuple[str, float]]) -> List[str]:
    return [document_id for document_id, _ in sorted(items, key=lambda item: (-item[1], item[0]))]


def reciprocal_rank_fusion(rankings: Sequence[Sequence[str]], constant: int = 60) -> Dict[str, float]:
    fused: Dict[str, float] = {}
    for ranking in rankings:
        for rank, document_id in enumerate(ranking, start=1):
            fused[document_id] = fused.get(document_id, 0.0) + 1.0 / (constant + rank)
    return fused


def decide_response(evidence: Sequence[Evidence], min_score: float, min_evidence: int) -> tuple[ResponseMode, str]:
    if not evidence:
        return ResponseMode.REFUSE, "no permitted evidence was retrieved"
    if len(evidence) < min_evidence:
        return ResponseMode.CLARIFY, "evidence coverage is too narrow for a stable answer"
    if evidence[0].score < min_score:
        return ResponseMode.REFUSE, "retrieval confidence is below policy threshold"
    return ResponseMode.ANSWER, "permitted evidence meets coverage and confidence policy"


def retrieve(
    query: str,
    documents: Sequence[Document],
    principals: FrozenSet[str],
    limit: int = 3,
    min_score: float = 0.02,
    min_evidence: int = 2,
) -> RetrievalResult:
    allowed = [document for document in documents if permitted(document, principals)]
    lexical = ranked_ids((document.document_id, lexical_score(query, document)) for document in allowed)
    semantic = ranked_ids((document.document_id, document.semantic_score) for document in allowed)
    fused = reciprocal_rank_fusion([lexical, semantic])
    by_id = {document.document_id: document for document in allowed}
    ordered = sorted(fused.items(), key=lambda item: (-item[1], item[0]))[:limit]
    evidence = tuple(
        Evidence(document_id=document_id, excerpt=by_id[document_id].text[:160], score=score)
        for document_id, score in ordered
        if lexical_score(query, by_id[document_id]) > 0 or by_id[document_id].semantic_score > 0
    )
    mode, reason = decide_response(evidence, min_score=min_score, min_evidence=min_evidence)
    return RetrievalResult(mode=mode, reason=reason, evidence=evidence)


if __name__ == "__main__":
    corpus = [
        Document("policy-1", "Approval is required before an irreversible action.", frozenset({"risk"}), 0.91),
        Document("runbook-1", "Every tool call emits an evidence event and named owner.", frozenset({"ops"}), 0.84),
        Document("public-1", "Read-only retrieval should preserve citations.", frozenset({"all"}), 0.72),
    ]
    result = retrieve("approval evidence", corpus, frozenset({"risk", "all"}))
    print(json.dumps({"mode": result.mode.value, "reason": result.reason, "evidence": [asdict(item) for item in result.evidence]}, indent=2))
