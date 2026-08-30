#!/usr/bin/env python3
"""Build sanitized technical-project packages, architecture SVGs, and website pages.

The supplied ZIP files are treated as untrusted input. Project code is never
executed. Only allow-listed text source files are selected; credentials,
customer datasets, model weights, generated dependencies, media, indexes and
deployment state are excluded or redacted.
"""

from __future__ import annotations

import hashlib
import html
import io
import json
import re
import shutil
import stat
import struct
import textwrap
import zipfile
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import quote, urlsplit
from xml.etree import ElementTree

from PIL import Image

from technical_project_catalog import PROJECTS


ROOT = Path(__file__).resolve().parents[1]
DOWNLOADS = Path.home() / "Downloads"
OUT_ROOT = ROOT / "samples" / "technical-projects"
BUILD_ROOT = ROOT / ".tmp-ai-projects.build"
PUBLIC_BUILD_ROOT = ROOT / ".tmp-technical-projects-public"
REFERENCE_PACK = DOWNLOADS / "IdeaStorm-Architecture-Image-Pack.zip"
SITE_BASE = "https://singhaditya21.github.io/Resume"
SOCIAL_IMAGE_URL = f"{SITE_BASE}/assets/social-preview.png"
CONTACT_EMAIL = "singhaditya21@gmail.com"

ALLOWED_SUFFIXES = {
    ".py", ".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".java", ".cs", ".go", ".rs",
    ".rb", ".php", ".sql", ".sh", ".ps1", ".html", ".css", ".scss", ".sass", ".less",
    ".vue", ".svelte", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", ".xml",
    ".graphql", ".gql", ".proto", ".properties", ".gradle", ".tf", ".hcl",
}
SPECIAL_FILES = {
    "dockerfile", "makefile", "procfile", "jenkinsfile", "gemfile", "pipfile", "go.mod",
    "go.sum", "cargo.toml", "cargo.lock", "requirements.txt", "pyproject.toml", "setup.py",
    "setup.cfg", "package.json", "go.mod", "cargo.toml",
    "tsconfig.json", ".gitignore", ".dockerignore", "alembic.ini",
}
EXCLUDED_SEGMENTS = {
    ".git", ".svn", ".hg", ".idea", ".vscode", ".claude", ".continue", ".vs", "node_modules",
    "bower_components", "vendor", ".venv", "venv", "env", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", ".next", "dist", "build", "coverage", "target", "bin", "obj",
    "models", "weights", "checkpoints", "recordings", "screenshots", "uploads", "logs", "runs",
    "evidence", "chroma", "vector_db", "vectorstore", "faiss_index", "ocr_cache", "backups",
    "secrets", ".ssh", ".aws", ".kube", "migrations", "migration", "seed", "seeds", "fixtures",
    "dataset", "datasets", "source_data", "raw", "contracts", "documents", "media", "docs",
}
EXCLUDED_PATH_TERMS = {
    ".git-credentials", "id_rsa", "id_ed25519", "known_hosts", "secrets.", "credential",
    "private_key", "private-key", ".pfx", ".pem", ".key", ".crt", ".cer", ".bak", ".gguf",
    ".onnx", ".pt", ".pth", ".pickle", ".pkl", ".sqlite", ".sqlite3", ".db", ".mp4", ".webm",
    ".mov", ".avi", ".mp3", ".wav", ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt",
    ".pptx", ".png", ".jpg", ".jpeg", ".gif", ".tif", ".tiff", ".zip", ".7z", ".tar",
    ".gz", ".dll", ".exe", ".so", ".dylib", ".class", ".jar", ".war", ".min.js", ".map",
    ".git_sync", "claude.md", "agents.md", "zone.identifier",
}
DATA_SEGMENTS = {"data", "dataset", "datasets", "source_data", "raw", "samples", "fixtures"}
RISKY_BASENAME_TERMS = {
    "credential", "secret", "private", "deploy", "deployment", "sync", "seed", "fixture", "sample_data",
    "customer_data", "employee", "contact", "user_mapping", "hierarchy", "production", "prod_config",
}
MAX_SOURCE_FILES = 24
MAX_SOURCE_BYTES = 2_500_000
MAX_FILE_BYTES = 600_000
MAX_PUBLIC_ZIP_BYTES = 95_000_000
MAX_REFERENCE_PNG_BYTES = 3_000_000
MAX_REFERENCE_TOTAL_BYTES = 20_000_000

SECRET_TOKEN_PATTERNS = [
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\bnvapi-[A-Za-z0-9_-]{16,}\b", re.I),
    re.compile(r"\bcsk-[A-Za-z0-9_-]{16,}\b", re.I),
    re.compile(r"\bgsk[_-][A-Za-z0-9_-]{16,}\b", re.I),
    re.compile(r"\bhf_[A-Za-z0-9]{16,}\b"),
    re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{16,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{16,}\b"),
    re.compile(r"AccountKey=[A-Za-z0-9+/=]{16,}", re.I),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b", re.I),
    re.compile(r"\b(?:sk|rk)_(?:live|test)_[A-Za-z0-9]{16,}\b", re.I),
]
PRIVATE_KEY_RE = re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----")
URL_CREDENTIAL_RE = re.compile(
    r"(?P<scheme>\b(?:https?|postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis)://)[^\s:/]+:[^\s@/]+@",
    re.I,
)
SECRET_KEY_FRAGMENT = r"(?:PASSWORD|PASSWD|PWD|API[_-]?KEY|SECRET|TOKEN|PRIVATE[_-]?KEY|CONSUMER[_-]?KEY|ACCESS[_-]?KEY|CLIENT[_-]?SECRET|AUTHORIZATION)"
QUOTED_SECRET_ASSIGNMENT_RE = re.compile(
    rf"(?im)(?P<prefix>['\"]?[A-Z0-9_.-]*{SECRET_KEY_FRAGMENT}[A-Z0-9_.-]*['\"]?\s*[:=]\s*)(?P<quote>['\"])(?P<value>[^'\"\r\n]{{1,}})(?P=quote)",
    re.I,
)
ENV_SECRET_ASSIGNMENT_RE = re.compile(
    rf"(?im)^(?P<prefix>\s*(?:export\s+)?[A-Z0-9_.-]*{SECRET_KEY_FRAGMENT}[A-Z0-9_.-]*\s*=\s*)(?P<value>[^\s#;]{{1,}})\s*$",
    re.I,
)
BEARER_RE = re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{18,}")
JWT_RE = re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b")
QUERY_SECRET_RE = re.compile(r"(?i)([?&](?:api[_-]?key|token|secret|access[_-]?token)=)[^&\s'\"<>]{8,}")
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
IPV4_RE = re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")
URL_RE = re.compile(r"https?://[^\s'\"<>)}\]]+", re.I)
LOCAL_PATH_RE = re.compile(r"(?:/Users/[^\s'\"]+|/home/[^\s'\"]+|[A-Za-z]:\\[^\r\n'\"]+)")
PHONE_RE = re.compile(r"(?<!\d)(?:\+?91[- .]?)?[6-9]\d{9}(?!\d)")
UUID_RE = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I)
CUSTOMER_NAME_RE = re.compile(
    r"\b(?:HDFC|SBI|PNB|Maybank|Kotak|Axis|ADIB|Arab Bank|Danamon|Dupaco|Westconsin|Magnifi|Max Life)\b",
    re.I,
)
OPAQUE_LITERAL_RE = re.compile(r"(?P<quote>['\"])(?P<value>[A-Za-z0-9_+/=-]{32,})(?P=quote)")
SENSITIVE_DATA_ASSIGNMENT_RE = re.compile(
    r"(?im)(?P<prefix>['\"]?[A-Z0-9_.-]*(?:CUSTOMER|CLIENT|EMPLOYEE|CONTACT|OWNER|MANAGER|ACCOUNT|PROJECT|USER)[_-]?(?:NAME|ID|CODE|EMAIL|PHONE)?[A-Z0-9_.-]*['\"]?\s*[:=]\s*)(?P<quote>['\"])(?P<value>[^'\"\r\n]{2,})(?P=quote)",
    re.I,
)
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
SAFE_URL_HOSTS = {
    "localhost", "127.0.0.1", "0.0.0.0", "example.com", "example.org", "example.invalid",
    "github.com", "raw.githubusercontent.com", "pypi.org", "npmjs.com", "registry.npmjs.org",
    "docs.python.org", "nodejs.org", "fastapi.tiangolo.com", "react.dev", "learn.microsoft.com",
    "www.w3.org",
}

CATEGORY_COLORS = {
    "Agentic AI & automation": ("#0b5bd3", "#63e6be"),
    "Knowledge, RAG & document AI": ("#6334b8", "#d7b8ff"),
    "Data & decision intelligence": ("#087f8c", "#7fe7dc"),
    "AI testing & quality": ("#d75a12", "#ffd199"),
    "Governance, risk & security": ("#157347", "#9be8b5"),
    "Enterprise operations": ("#263a8b", "#9bb2ff"),
    "Concept / source unavailable": ("#7b4b13", "#ffd48a"),
}

SOURCE_ROLE_RULES = (
    ("AI / retrieval", re.compile(r"(?i)\b(?:llm|openai|ollama|embedding|vector|retriev|rag|prompt|model|inference|rerank)")),
    ("Service / API", re.compile(r"(?i)\b(?:fastapi|flask|express|route|router|endpoint|request|response|controller|service)")),
    ("Workflow / orchestration", re.compile(r"(?i)\b(?:agent|pipeline|workflow|orchestrat|scheduler|queue|worker|state machine)")),
    ("Data / persistence", re.compile(r"(?i)\b(?:postgres|sql|database|schema|repository|milvus|chroma|redis|kafka|rabbitmq)")),
    ("Control / validation", re.compile(r"(?i)\b(?:auth|acl|rbac|policy|guard|validat|audit|permission|encrypt|sanitize|refus|limit)")),
    ("Test / quality", re.compile(r"(?i)\b(?:pytest|unittest|describe\s*\(|it\s*\(|assert|playwright|test case|expect\s*\()")),
    ("User experience", re.compile(r"(?i)\b(?:react|component|render|dashboard|streamlit|websocket|server.sent|eventsource|jsx|tsx)")),
    ("Operations / delivery", re.compile(r"(?i)\b(?:docker|kubernetes|openshift|jenkins|prometheus|nginx|caddy|healthcheck|deploy)")),
)


def safe_entry(name: str) -> bool:
    path = PurePosixPath(name)
    return not path.is_absolute() and ".." not in path.parts


def is_symlink(info: zipfile.ZipInfo) -> bool:
    mode = (info.external_attr >> 16) & 0xFFFF
    return stat.S_ISLNK(mode)


def write_text_lf(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ensure_within(path: Path, parent: Path) -> Path:
    resolved = path.resolve()
    base = parent.resolve()
    if resolved != base and base not in resolved.parents:
        raise RuntimeError(f"Unsafe output path outside {base}: {resolved}")
    return resolved


def validate_catalog(projects: list[dict]) -> None:
    seen_slugs: set[str] = set()
    seen_archives: set[str] = set()
    required = {"slug", "name", "archive", "category", "evidence_level", "summary", "flow", "components", "evidence"}
    for project in projects:
        missing = required - set(project)
        if missing:
            raise RuntimeError(f"Catalog entry is missing {sorted(missing)}: {project.get('name', '<unnamed>')}")
        slug = project["slug"]
        archive_name = project["archive"]
        if not SLUG_RE.fullmatch(slug) or slug in seen_slugs:
            raise RuntimeError(f"Unsafe or duplicate project slug: {slug}")
        archive_path = PurePosixPath(archive_name)
        if archive_path.name != archive_name or archive_path.suffix.lower() != ".zip" or archive_name in seen_archives:
            raise RuntimeError(f"Unsafe or duplicate archive name: {archive_name}")
        archive = DOWNLOADS / archive_name
        if not archive.is_file() or not zipfile.is_zipfile(archive):
            raise RuntimeError(f"Missing or invalid source archive: {archive}")
        seen_slugs.add(slug)
        seen_archives.add(archive_name)


def source_priority(name: str) -> int:
    path = PurePosixPath(name)
    lower = name.lower()
    base = path.name.lower()
    suffix = path.suffix.lower()
    parts = {p.lower() for p in path.parts}
    if any(part in EXCLUDED_SEGMENTS for part in parts):
        return -1
    if any(term in lower for term in EXCLUDED_PATH_TERMS):
        return -1
    if base == ".env" or base.startswith(".env."):
        return -1
    if any(re.search(rf"(^|[-_.]){re.escape(term)}($|[-_.])", base) for term in RISKY_BASENAME_TERMS):
        return -1
    if parts & DATA_SEGMENTS:
        if suffix == ".json" and any(term in base for term in ("schema", "config", "manifest", "contract", "workflow")):
            return 45
        return -1
    if base in SPECIAL_FILES or re.fullmatch(r"requirements(?:-[a-z0-9_.-]+)?\.txt", base):
        return 100
    if suffix not in ALLOWED_SUFFIXES:
        return -1
    if suffix == ".sql":
        return 45
    if "test" in parts or "tests" in parts or re.search(r"(^|/)(test|spec)[_.-]", lower):
        return 80
    if parts & {"src", "app", "backend", "frontend", "server", "services", "agents", "packages", "scripts", "infra", "deploy"}:
        return 90
    return 60


def decode_text(data: bytes) -> str | None:
    if b"\x00" in data[:8192]:
        return None
    text = data.decode("utf-8", errors="replace")
    if text and text.count("\ufffd") / len(text) > 0.02:
        return None
    return text


def looks_generated_or_minified(text: str) -> bool:
    if len(text) < 80_000:
        return False
    lines = text.splitlines() or [text]
    average = len(text) / max(1, len(lines))
    longest = max(len(line) for line in lines)
    return len(lines) < 80 or average > 420 or longest > 12_000


def placeholder_literal(value: str) -> bool:
    normalized = value.strip().lower()
    return bool(re.search(
        r"^(?:your[_ -]|replace|change|example|dummy|test|none|null|false|true|redacted|placeholder|portfolio|\$\{|<|process\.env|os\.getenv)",
        normalized,
    ))


def sanitize_text(text: str) -> tuple[str | None, list[str]]:
    findings: list[str] = []
    if PRIVATE_KEY_RE.search(text):
        return None, ["private key block removed with file"]

    for pattern in SECRET_TOKEN_PATTERNS:
        if pattern.search(text):
            text = pattern.sub("REDACTED_SECRET", text)
            findings.append("credential token")
    if BEARER_RE.search(text):
        text = BEARER_RE.sub("Bearer REDACTED_SECRET", text)
        findings.append("bearer credential")
    if JWT_RE.search(text):
        text = JWT_RE.sub("REDACTED_JWT", text)
        findings.append("JWT credential")
    if URL_CREDENTIAL_RE.search(text):
        text = URL_CREDENTIAL_RE.sub(lambda match: f"{match.group('scheme')}portfolio:REDACTED_SECRET@", text)
        findings.append("embedded URL credential")
    if QUERY_SECRET_RE.search(text):
        text = QUERY_SECRET_RE.sub(r"\1REDACTED_SECRET", text)
        findings.append("query-string credential")

    def replace_quoted_secret(match: re.Match[str]) -> str:
        if match.group("value").strip().lower().startswith("redacted"):
            return match.group(0)
        findings.append("hard-coded secret assignment")
        quote = match.group("quote")
        return f"{match.group('prefix')}{quote}REDACTED_SECRET{quote}"

    def replace_env_secret(match: re.Match[str]) -> str:
        if match.group("value").strip().lower().startswith("redacted"):
            return match.group(0)
        findings.append("hard-coded environment secret")
        return f"{match.group('prefix')}REDACTED_SECRET"

    def replace_sensitive_value(match: re.Match[str]) -> str:
        value = match.group("value")
        if placeholder_literal(value) or any(marker in value for marker in ("${", "{{", "<%")):
            return match.group(0)
        findings.append("customer or identity literal")
        quote = match.group("quote")
        return f"{match.group('prefix')}{quote}PORTFOLIO_REDACTED{quote}"

    def replace_opaque_literal(match: re.Match[str]) -> str:
        value = match.group("value")
        if value.lower().startswith("redacted") or len(set(value.lower())) < 8:
            return match.group(0)
        findings.append("opaque high-entropy literal")
        quote = match.group("quote")
        return f"{quote}REDACTED_OPAQUE_VALUE{quote}"

    text = QUOTED_SECRET_ASSIGNMENT_RE.sub(replace_quoted_secret, text)
    text = ENV_SECRET_ASSIGNMENT_RE.sub(replace_env_secret, text)
    text = SENSITIVE_DATA_ASSIGNMENT_RE.sub(replace_sensitive_value, text)
    text = OPAQUE_LITERAL_RE.sub(replace_opaque_literal, text)
    if EMAIL_RE.search(text):
        text = EMAIL_RE.sub("portfolio@example.invalid", text)
        findings.append("email address")
    if PHONE_RE.search(text):
        text = PHONE_RE.sub("0000000000", text)
        findings.append("phone number")
    if UUID_RE.search(text):
        text = UUID_RE.sub("00000000-0000-0000-0000-000000000000", text)
        findings.append("unique identifier")
    if CUSTOMER_NAME_RE.search(text):
        text = CUSTOMER_NAME_RE.sub("CUSTOMER_REDACTED", text)
        findings.append("customer name")

    def replace_ip(match: re.Match[str]) -> str:
        value = match.group(0)
        if value in {"127.0.0.1", "0.0.0.0", "192.0.2.10"}:
            return value
        findings.append("network address")
        return "192.0.2.10"

    text = IPV4_RE.sub(replace_ip, text)

    def replace_url(match: re.Match[str]) -> str:
        value = match.group(0)
        try:
            host = (urlsplit(value).hostname or "").lower()
        except ValueError:
            host = ""
        if host in SAFE_URL_HOSTS or host.endswith((".github.com", ".microsoft.com")):
            return value
        findings.append("non-public service URL")
        return "https://example.invalid"

    text = URL_RE.sub(replace_url, text)
    if LOCAL_PATH_RE.search(text):
        text = LOCAL_PATH_RE.sub("/opt/portfolio/project", text)
        findings.append("local filesystem path")
    return text, sorted(set(findings))


def unresolved_sensitive_findings(text: str, *, include_opaque: bool = False) -> list[str]:
    findings: list[str] = []
    if PRIVATE_KEY_RE.search(text):
        findings.append("private key")
    for pattern in SECRET_TOKEN_PATTERNS:
        if pattern.search(text):
            findings.append("credential token")
    if BEARER_RE.search(text) or JWT_RE.search(text):
        findings.append("bearer or JWT credential")
    if URL_CREDENTIAL_RE.search(text) or QUERY_SECRET_RE.search(text):
        findings.append("credential-bearing URL")
    for pattern in (QUOTED_SECRET_ASSIGNMENT_RE, ENV_SECRET_ASSIGNMENT_RE):
        for match in pattern.finditer(text):
            if not match.group("value").strip().lower().startswith("redacted"):
                findings.append("hard-coded secret assignment")
                break
    if EMAIL_RE.search(text):
        findings.append("email address")
    if PHONE_RE.search(text):
        findings.append("phone number")
    if UUID_RE.search(text):
        findings.append("unique identifier")
    if CUSTOMER_NAME_RE.search(text):
        findings.append("customer name")
    if LOCAL_PATH_RE.search(text):
        findings.append("local filesystem path")
    if include_opaque:
        for match in OPAQUE_LITERAL_RE.finditer(text):
            value = match.group("value")
            if not value.lower().startswith("redacted") and len(set(value.lower())) >= 8:
                findings.append("opaque high-entropy literal")
                break
    for match in URL_RE.finditer(text):
        try:
            host = (urlsplit(match.group(0)).hostname or "").lower()
        except ValueError:
            host = ""
        if host not in SAFE_URL_HOSTS and not host.endswith((".github.com", ".microsoft.com")):
            findings.append("non-public service URL")
            break
    return sorted(set(findings))


def eligible_source(zf: zipfile.ZipFile, info: zipfile.ZipInfo) -> tuple[int, str] | None:
    if info.is_dir() or is_symlink(info) or not safe_entry(info.filename):
        return None
    priority = source_priority(info.filename)
    if priority < 0 or info.file_size > MAX_FILE_BYTES:
        return None
    if PurePosixPath(info.filename).suffix.lower() == ".sql" and info.file_size > 600_000:
        return None
    return priority, info.filename


def source_roles(text: str, suffix: str) -> list[str]:
    """Describe an anonymized sample without retaining its original member path."""
    roles = [label for label, pattern in SOURCE_ROLE_RULES if pattern.search(text)]
    if suffix in {".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", ".tf", ".hcl"}:
        roles.append("Configuration / infrastructure")
    if suffix in {".html", ".css", ".scss", ".vue", ".svelte"}:
        roles.append("User experience")
    return list(dict.fromkeys(roles))[:4] or ["General implementation / configuration"]


def select_and_sanitize_source(project: dict, stage_source: Path) -> dict:
    archive = DOWNLOADS / project["archive"]
    included: list[str] = []
    included_details: list[dict] = []
    redactions: dict[str, list[str]] = {}
    excluded = Counter()
    source_kinds = Counter()
    selected_bytes = 0
    stage_source.mkdir(parents=True, exist_ok=True)
    evidence_hints = [item.replace("\\", "/").strip("/").lower() for item in project["evidence"]]

    def evidence_boost(name: str) -> int:
        lower_name = name.replace("\\", "/").lower()
        boost = 0
        for hint in evidence_hints:
            if not hint:
                continue
            if hint.endswith("/") and hint in lower_name:
                boost = max(boost, 260)
            elif lower_name.endswith(hint):
                boost = max(boost, 320)
            elif PurePosixPath(lower_name).name == PurePosixPath(hint).name:
                boost = max(boost, 220)
        return boost

    with zipfile.ZipFile(archive) as zf:
        candidates = []
        member_names: set[str] = set()
        for info in zf.infolist():
            normalized_name = info.filename.replace("\\", "/")
            if normalized_name in member_names:
                excluded["duplicate archive member"] += 1
                continue
            member_names.add(normalized_name)
            candidate = eligible_source(zf, info)
            if candidate is None:
                excluded["not allow-listed, generated, binary, data, secret file or oversized"] += 1
                continue
            score = candidate[0] + evidence_boost(candidate[1])
            candidates.append((score, info.file_size, candidate[1], info))
        candidates.sort(key=lambda item: (-item[0], item[1], item[2].lower()))
        sql_count = 0
        for _, _, name, info in candidates:
            if len(included) >= MAX_SOURCE_FILES or selected_bytes + info.file_size > MAX_SOURCE_BYTES:
                excluded["portfolio size cap"] += 1
                continue
            suffix = PurePosixPath(name).suffix.lower()
            if suffix == ".sql" and sql_count >= 3:
                excluded["SQL sample cap"] += 1
                continue
            try:
                data = zf.read(info)
            except Exception:
                excluded["read failure"] += 1
                continue
            text = decode_text(data)
            if text is None:
                excluded["non-text content"] += 1
                continue
            if looks_generated_or_minified(text):
                excluded["generated or minified text"] += 1
                continue
            if suffix == ".sql":
                if len(re.findall(r"(?i)\b(?:insert\s+into|copy\s+.+from\s+stdin)\b", text)) > 15:
                    excluded["data-bearing SQL"] += 1
                    continue
            sanitized, changes = sanitize_text(text)
            if sanitized is None:
                excluded["private key material"] += 1
                continue
            unresolved = unresolved_sensitive_findings(sanitized, include_opaque=True)
            if unresolved:
                excluded["unresolved sensitive content"] += 1
                continue
            sanitized_bytes = len(sanitized.encode("utf-8"))
            if sanitized_bytes > MAX_FILE_BYTES or selected_bytes + sanitized_bytes > MAX_SOURCE_BYTES:
                excluded["post-redaction size cap"] += 1
                continue
            public_name = f"sample-{len(included) + 1:02d}{suffix or '.txt'}"
            destination = stage_source / public_name
            write_text_lf(destination, sanitized)
            public_path = f"source/{public_name}"
            meaningful = bool(sanitized.strip())
            included.append(public_path)
            included_details.append({
                "file": public_path,
                "bytes": sanitized_bytes,
                "meaningful": meaningful,
                "roles": source_roles(sanitized, suffix),
            })
            selected_bytes += sanitized_bytes
            source_kinds[suffix or "no-extension"] += 1
            if suffix == ".sql":
                sql_count += 1
            if changes:
                redactions[f"source/{public_name}"] = changes
    if project["evidence_level"] != "concept" and not included:
        raise RuntimeError(f"No safe source samples could be selected for {project['name']}")
    non_empty_count = sum(item["meaningful"] for item in included_details)
    return {
        "source_archive": project["archive"],
        "source_archive_sha256": sha256_file(archive),
        "included_files": included,
        "included_file_details": included_details,
        "included_file_count": len(included),
        "non_empty_file_count": non_empty_count,
        "empty_file_count": len(included_details) - non_empty_count,
        "meaningful_bytes": sum(item["bytes"] for item in included_details if item["meaningful"]),
        "included_bytes": selected_bytes,
        "source_types": dict(sorted(source_kinds.items())),
        "redacted_files": redactions,
        "excluded_counts": dict(excluded),
    }


def svg_escape(value: str) -> str:
    return html.escape(str(value), quote=True)


def wrap(value: str, width: int = 22, max_lines: int = 3) -> list[str]:
    lines = textwrap.wrap(str(value), width=width, break_long_words=True, break_on_hyphens=True) or [""]
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip(" .") + "…"
    return lines


def text_lines(x: float, y: float, value: str, width: int, size: int, color: str, weight: int = 600,
               anchor: str = "middle", max_lines: int = 3, line_height: int | None = None) -> str:
    line_height = line_height or int(size * 1.18)
    lines = wrap(value, width, max_lines)
    tspans = []
    for index, line in enumerate(lines):
        dy = 0 if index == 0 else line_height
        tspans.append(f'<tspan x="{x}" dy="{dy}">{svg_escape(line)}</tspan>')
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{color}">{"".join(tspans)}</text>'


def svg_shell(project: dict, subtitle: str, body: str, footer: str) -> str:
    accent, accent_soft = CATEGORY_COLORS.get(project["category"], CATEGORY_COLORS["Enterprise operations"])
    concept = project["evidence_level"] == "concept"
    label = "CONCEPTUAL — SOURCE ARCHIVE INCOMPLETE" if concept else project["evidence_label"].upper()
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900" role="img" aria-labelledby="title desc">
<title id="title">{svg_escape(project['name'])} architecture</title><desc id="desc">{svg_escape(subtitle)}</desc>
<defs><linearGradient id="header" x1="0" x2="1"><stop stop-color="#071b38"/><stop offset="1" stop-color="{accent}"/></linearGradient><filter id="shadow"><feDropShadow dx="0" dy="5" stdDeviation="8" flood-opacity=".13"/></filter><marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#173c78"/></marker><pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse"><path d="M36 0H0V36" fill="none" stroke="#d9e3f0" stroke-width="1"/></pattern></defs>
<rect width="1600" height="900" fill="#f5f8fc"/><rect width="1600" height="900" fill="url(#grid)" opacity=".35"/>
<rect width="1600" height="126" fill="url(#header)"/><text x="70" y="58" font-family="Inter,Arial,sans-serif" font-size="42" font-weight="800" fill="white">{svg_escape(project['name'].upper())}</text><text x="70" y="96" font-family="Inter,Arial,sans-serif" font-size="22" font-weight="600" fill="{accent_soft}">{svg_escape(subtitle)}</text>
<rect x="1210" y="35" width="320" height="48" rx="24" fill="{'#9a3412' if concept else '#ffffff'}" opacity=".98"/><text x="1370" y="65" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-size="15" font-weight="800" fill="{'#ffffff' if concept else accent}">{svg_escape(label)}</text>
<g font-family="Inter,Arial,sans-serif">{body}</g>
<rect x="58" y="828" width="1484" height="48" rx="12" fill="#071b38"/><text x="800" y="859" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-size="19" font-weight="750" fill="white">{svg_escape(footer)}</text>
</svg>'''


def architecture_overview(project: dict) -> str:
    accent, _ = CATEGORY_COLORS.get(project["category"], CATEGORY_COLORS["Enterprise operations"])
    layers = [
        ("01", "EXPERIENCE", project["components"]["experience"]),
        ("02", "APPLICATION", project["components"]["services"]),
        ("03", "AI / AUTOMATION", project["components"]["ai"]),
        ("04", "DATA & INTEGRATION", project["components"]["data"]),
        ("05", "OPERATIONS & CONTROL", project["components"]["operations"]),
    ]
    body = []
    y = 151
    for number, title, nodes in layers:
        nodes = (nodes or ["No implementation evidence supplied"])[:5]
        body.append(f'<rect x="58" y="{y}" width="1484" height="118" rx="16" fill="white" stroke="#c8d6e8" filter="url(#shadow)"/>')
        body.append(f'<rect x="58" y="{y}" width="225" height="118" rx="16" fill="{accent}"/>')
        body.append(f'<text x="92" y="{y+47}" font-size="31" font-weight="850" fill="white">{number}</text><text x="92" y="{y+80}" font-size="16" font-weight="800" fill="white">{svg_escape(title)}</text>')
        start_x, available = 318, 1184
        gap = 18
        node_w = (available - gap * (len(nodes) - 1)) / len(nodes)
        for idx, node in enumerate(nodes):
            x = start_x + idx * (node_w + gap)
            body.append(f'<rect x="{x:.1f}" y="{y+25}" width="{node_w:.1f}" height="68" rx="11" fill="#f7faff" stroke="#99b4d6"/>')
            body.append(text_lines(x + node_w/2, y+54, node, 21, 17, "#0d294f", 700, max_lines=2, line_height=19))
            if idx < len(nodes)-1:
                body.append(f'<line x1="{x+node_w+3:.1f}" y1="{y+59}" x2="{x+node_w+gap-3:.1f}" y2="{y+59}" stroke="#173c78" stroke-width="2" marker-end="url(#arrow)"/>')
        y += 131
    return svg_shell(project, "Executive technical architecture", "".join(body), project["architecture_thesis"])


def runtime_flow(project: dict) -> str:
    accent, soft = CATEGORY_COLORS.get(project["category"], CATEGORY_COLORS["Enterprise operations"])
    flow = project["flow"][:6]
    body = [f'<text x="70" y="177" font-size="20" font-weight="800" fill="{accent}">PRIMARY REQUEST / DATA PATH</text>']
    start_x, y, node_w, gap = 72, 235, 215, 38
    for idx, node in enumerate(flow):
        x = start_x + idx * (node_w + gap)
        body.append(f'<rect x="{x}" y="{y}" width="{node_w}" height="125" rx="18" fill="white" stroke="{accent}" stroke-width="2" filter="url(#shadow)"/>')
        body.append(f'<circle cx="{x+31}" cy="{y+31}" r="19" fill="{accent}"/><text x="{x+31}" y="{y+38}" text-anchor="middle" font-size="18" font-weight="850" fill="white">{idx+1}</text>')
        body.append(text_lines(x+node_w/2, y+69, node, 20, 18, "#0d294f", 750, max_lines=3, line_height=22))
        if idx < len(flow)-1:
            body.append(f'<line x1="{x+node_w+5}" y1="{y+62}" x2="{x+node_w+gap-6}" y2="{y+62}" stroke="#173c78" stroke-width="3" marker-end="url(#arrow)"/>')
    body.append(f'<rect x="72" y="430" width="1456" height="305" rx="24" fill="#eef5ff" stroke="#b7cae4"/>')
    body.append(f'<text x="104" y="475" font-size="21" font-weight="800" fill="{accent}">CROSS-CUTTING CONTROLS</text>')
    controls = project["controls"][:4]
    for idx, control in enumerate(controls):
        x = 104 + (idx % 2) * 710
        cy = 530 + (idx // 2) * 90
        body.append(f'<rect x="{x}" y="{cy}" width="660" height="66" rx="13" fill="white" stroke="#c7d6e8"/>')
        body.append(f'<rect x="{x}" y="{cy}" width="9" height="66" rx="5" fill="{soft}"/>')
        body.append(text_lines(x+34, cy+29, control, 58, 18, "#17314f", 700, anchor="start", max_lines=2, line_height=21))
    return svg_shell(project, "Runtime and request architecture", "".join(body), "Bounded execution, explicit evidence, and a human-owned outcome.")


def system_context(project: dict) -> str:
    accent, soft = CATEGORY_COLORS.get(project["category"], CATEGORY_COLORS["Enterprise operations"])
    columns = [
        ("USERS & CHANNELS", project["components"]["experience"][:4]),
        ("SYSTEM CORE", project["components"]["services"][:4]),
        ("AI, DATA & INTEGRATIONS", (project["components"]["ai"] + project["components"]["data"])[:4]),
    ]
    body = []
    for col_idx, (title, nodes) in enumerate(columns):
        x = 70 + col_idx * 510
        body.append(f'<rect x="{x}" y="190" width="450" height="470" rx="22" fill="white" stroke="#b9cbe2" filter="url(#shadow)"/>')
        body.append(f'<rect x="{x}" y="190" width="450" height="66" rx="22" fill="{accent}"/><text x="{x+225}" y="231" text-anchor="middle" font-size="19" font-weight="850" fill="white">{svg_escape(title)}</text>')
        for idx, node in enumerate(nodes or ["No source evidence supplied"]):
            y = 287 + idx * 82
            body.append(f'<rect x="{x+38}" y="{y}" width="374" height="59" rx="12" fill="#f4f8fd" stroke="#9db8da"/>')
            body.append(text_lines(x+225, y+26, node, 42, 17, "#17314f", 720, max_lines=2, line_height=19))
        if col_idx < 2:
            body.append(f'<line x1="{x+457}" y1="425" x2="{x+500}" y2="425" stroke="#173c78" stroke-width="4" marker-end="url(#arrow)"/>')
    body.append(f'<rect x="70" y="694" width="1470" height="96" rx="18" fill="#071b38"/><text x="110" y="731" font-size="18" font-weight="850" fill="{soft}">DEPLOYMENT &amp; OPERATING SURFACE</text>')
    ops = project["components"]["operations"][:5] or ["Deployment evidence not supplied"]
    node_w = 250
    for idx, node in enumerate(ops):
        x = 110 + idx * 280
        body.append(f'<rect x="{x}" y="746" width="{node_w}" height="31" rx="8" fill="white" opacity=".95"/>')
        body.append(text_lines(x+node_w/2, 767, node, 26, 14, "#17314f", 750, max_lines=1))
    return svg_shell(project, "System context and deployment", "".join(body), "Clear system ownership, explicit external boundaries, and deployable operational controls.")


def authenticated_lifecycle(project: dict) -> str:
    accent, soft = CATEGORY_COLORS.get(project["category"], CATEGORY_COLORS["Enterprise operations"])
    lifecycle = ["Identity / request", *project["flow"][:5], "Evidence / outcome"][:7]
    body = [f'<text x="70" y="177" font-size="20" font-weight="800" fill="{accent}">AUTHENTICATED OR GOVERNED REQUEST LIFECYCLE</text>']
    for idx, step in enumerate(lifecycle):
        x = 72 + idx * 214
        y = 250 if idx % 2 == 0 else 430
        body.append(f'<circle cx="{x+77}" cy="{y}" r="57" fill="white" stroke="{accent}" stroke-width="4" filter="url(#shadow)"/>')
        body.append(f'<circle cx="{x+77}" cy="{y}" r="24" fill="{soft}"/><text x="{x+77}" y="{y+7}" text-anchor="middle" font-size="20" font-weight="850" fill="#17314f">{idx+1}</text>')
        body.append(text_lines(x+77, y+85, step, 20, 17, "#17314f", 760, max_lines=3, line_height=19))
        if idx < len(lifecycle)-1:
            nx = 72 + (idx+1) * 214 + 20
            ny = 250 if (idx+1) % 2 == 0 else 430
            body.append(f'<path d="M{x+134},{y} C{x+165},{y} {nx-30},{ny} {nx},{ny}" fill="none" stroke="#173c78" stroke-width="3" marker-end="url(#arrow)"/>')
    body.append(f'<rect x="72" y="650" width="1456" height="135" rx="20" fill="#eef5ff" stroke="#b7cae4"/><text x="106" y="690" font-size="18" font-weight="850" fill="{accent}">LIFECYCLE GATES</text>')
    for idx, control in enumerate(project["controls"][:4]):
        x = 106 + idx * 350
        body.append(f'<rect x="{x}" y="712" width="316" height="48" rx="10" fill="white" stroke="#b7cae4"/>')
        body.append(text_lines(x+158, 733, control, 34, 14, "#17314f", 700, max_lines=2, line_height=16))
    return svg_shell(project, "Authenticated and governed request lifecycle", "".join(body), "Identity, scope, policy and evidence remain explicit from request to outcome.")


def data_architecture(project: dict) -> str:
    accent, soft = CATEGORY_COLORS.get(project["category"], CATEGORY_COLORS["Enterprise operations"])
    domains = (project["components"]["data"] + project["components"]["services"])[:6]
    center = project["components"]["data"][0] if project["components"]["data"] else "Application state"
    positions = [(155,235),(560,190),(965,235),(155,475),(560,520),(965,475)]
    body = [
        f'<text x="70" y="177" font-size="20" font-weight="800" fill="{accent}">DATA DOMAINS, SYSTEM OF RECORD, AND READ PATH</text>',
        f'<ellipse cx="800" cy="400" rx="225" ry="115" fill="white" stroke="{accent}" stroke-width="4" filter="url(#shadow)"/>',
        f'<ellipse cx="800" cy="365" rx="225" ry="58" fill="{soft}" opacity=".75"/>',
        text_lines(800, 396, center, 25, 25, "#17314f", 850, max_lines=2, line_height=28),
        '<text x="800" y="458" text-anchor="middle" font-size="16" font-weight="700" fill="#58708f">governed application state</text>',
    ]
    for idx, item in enumerate(domains or ["No data evidence supplied"]):
        x, y = positions[idx]
        body.append(f'<rect x="{x}" y="{y}" width="300" height="88" rx="16" fill="white" stroke="#9db8da" filter="url(#shadow)"/>')
        body.append(text_lines(x+150, y+36, item, 32, 18, "#17314f", 760, max_lines=2, line_height=21))
        body.append(f'<line x1="{x+150}" y1="{y+88 if y<400 else y}" x2="800" y2="{340 if y<400 else 470}" stroke="#7697bf" stroke-width="2" stroke-dasharray="6 6"/>')
    body.append(f'<rect x="72" y="678" width="1456" height="108" rx="18" fill="#071b38"/><text x="108" y="717" font-size="18" font-weight="850" fill="{soft}">READ / ANALYTICS PATH</text>')
    read_flow = project["flow"][-4:]
    for idx, step in enumerate(read_flow):
        x = 108 + idx * 348
        body.append(f'<rect x="{x}" y="735" width="312" height="34" rx="8" fill="white"/>')
        body.append(text_lines(x+156, 757, step, 34, 14, "#17314f", 730, max_lines=1))
    return svg_shell(project, "Data architecture and governed read path", "".join(body), "Separate source truth, derived intelligence, and the evidence returned to users.")


def workflow_architecture(project: dict) -> str:
    accent, soft = CATEGORY_COLORS.get(project["category"], CATEGORY_COLORS["Enterprise operations"])
    body = [
        f'<text x="70" y="177" font-size="20" font-weight="800" fill="{accent}">DETERMINISTIC AND AI-ASSISTED WORKFLOWS</text>',
        '<rect x="72" y="220" width="1456" height="230" rx="22" fill="white" stroke="#b7cae4" filter="url(#shadow)"/>',
        f'<rect x="72" y="220" width="245" height="230" rx="22" fill="{accent}"/><text x="194" y="309" text-anchor="middle" font-size="23" font-weight="850" fill="white">PRIMARY</text><text x="194" y="341" text-anchor="middle" font-size="17" font-weight="750" fill="white">EXECUTION LANE</text>',
    ]
    lane = project["flow"][:5]
    for idx, step in enumerate(lane):
        x = 350 + idx * 225
        body.append(f'<rect x="{x}" y="292" width="190" height="78" rx="13" fill="#f4f8fd" stroke="#9db8da"/>')
        body.append(text_lines(x+95, 326, step, 21, 16, "#17314f", 730, max_lines=2, line_height=18))
        if idx < len(lane)-1:
            body.append(f'<line x1="{x+194}" y1="331" x2="{x+219}" y2="331" stroke="#173c78" stroke-width="3" marker-end="url(#arrow)"/>')
    body.extend([
        '<rect x="72" y="480" width="1456" height="230" rx="22" fill="#eef5ff" stroke="#b7cae4" filter="url(#shadow)"/>',
        f'<rect x="72" y="480" width="245" height="230" rx="22" fill="#071b38"/><text x="194" y="569" text-anchor="middle" font-size="23" font-weight="850" fill="{soft}">ASSISTED</text><text x="194" y="601" text-anchor="middle" font-size="17" font-weight="750" fill="white">INTELLIGENCE LANE</text>',
    ])
    assisted = (project["components"]["ai"] + ["Human review", "Audit / learn"])[:5]
    for idx, step in enumerate(assisted):
        x = 350 + idx * 225
        body.append(f'<rect x="{x}" y="552" width="190" height="78" rx="13" fill="white" stroke="{accent}"/>')
        body.append(text_lines(x+95, 586, step, 21, 16, "#17314f", 730, max_lines=2, line_height=18))
        if idx < len(assisted)-1:
            body.append(f'<line x1="{x+194}" y1="591" x2="{x+219}" y2="591" stroke="#173c78" stroke-width="3" marker-end="url(#arrow)"/>')
    return svg_shell(project, "Workflow and orchestration architecture", "".join(body), "Deterministic services own facts; assisted intelligence proposes; accountable people decide.")


def ai_control_plane(project: dict) -> str:
    accent, soft = CATEGORY_COLORS.get(project["category"], CATEGORY_COLORS["Enterprise operations"])
    ai_nodes = project["components"]["ai"][:5] or ["No runtime AI evidenced"]
    body = [
        f'<text x="70" y="177" font-size="20" font-weight="800" fill="{accent}">AI / AUTOMATION RESPONSIBILITY BOUNDARY</text>',
        '<rect x="70" y="215" width="310" height="500" rx="22" fill="white" stroke="#bfd0e5" filter="url(#shadow)"/>',
        '<text x="225" y="260" text-anchor="middle" font-size="20" font-weight="800" fill="#17314f">INPUTS &amp; CONTEXT</text>',
    ]
    for idx, item in enumerate((project["components"]["experience"] + project["components"]["data"])[:5]):
        y = 292 + idx * 73
        body.append(f'<rect x="102" y="{y}" width="246" height="53" rx="12" fill="#f4f8fd" stroke="#a9bfdc"/>')
        body.append(text_lines(225, y+24, item, 27, 16, "#17314f", 700, max_lines=2, line_height=18))
    body.extend([
        f'<line x1="390" y1="465" x2="500" y2="465" stroke="#173c78" stroke-width="4" marker-end="url(#arrow)"/>',
        f'<rect x="510" y="215" width="580" height="500" rx="22" fill="#edf5ff" stroke="{accent}" stroke-width="2" filter="url(#shadow)"/>',
        f'<text x="800" y="260" text-anchor="middle" font-size="21" font-weight="850" fill="{accent}">CONTROLLED INTELLIGENCE PLANE</text>',
    ])
    for idx, item in enumerate(ai_nodes):
        y = 294 + idx * 77
        body.append(f'<rect x="555" y="{y}" width="490" height="56" rx="13" fill="white" stroke="#a9bfdc"/>')
        body.append(f'<circle cx="586" cy="{y+28}" r="16" fill="{soft}"/><text x="586" y="{y+34}" text-anchor="middle" font-size="15" font-weight="850" fill="#17314f">{idx+1}</text>')
        body.append(text_lines(620, y+25, item, 47, 17, "#17314f", 750, anchor="start", max_lines=2, line_height=19))
    body.extend([
        f'<line x1="1100" y1="465" x2="1210" y2="465" stroke="#173c78" stroke-width="4" marker-end="url(#arrow)"/>',
        '<rect x="1220" y="215" width="310" height="500" rx="22" fill="white" stroke="#bfd0e5" filter="url(#shadow)"/>',
        '<text x="1375" y="260" text-anchor="middle" font-size="20" font-weight="800" fill="#17314f">OUTPUT &amp; OWNERSHIP</text>',
    ])
    outputs = (project.get("outputs") or ["Evidence-backed result", "Human review", "Audit record", "Operational action"])[:5]
    for idx, item in enumerate(outputs):
        y = 292 + idx * 73
        body.append(f'<rect x="1252" y="{y}" width="246" height="53" rx="12" fill="#f4f8fd" stroke="#a9bfdc"/>')
        body.append(text_lines(1375, y+24, item, 27, 16, "#17314f", 700, max_lines=2, line_height=18))
    return svg_shell(project, "AI, agent and automation control plane", "".join(body), project["ai_role"])


def trust_boundaries(project: dict) -> str:
    accent, soft = CATEGORY_COLORS.get(project["category"], CATEGORY_COLORS["Enterprise operations"])
    zones = [
        ("ZONE 0", "USER / EXTERNAL INPUT", project["components"]["experience"][:3]),
        ("ZONE 1", "APPLICATION BOUNDARY", project["components"]["services"][:3]),
        ("ZONE 2", "AI / AUTOMATION BOUNDARY", project["components"]["ai"][:3] or ["No runtime AI evidenced"]),
        ("ZONE 3", "DATA / OPERATIONS BOUNDARY", (project["components"]["data"] + project["components"]["operations"])[:3]),
    ]
    body = []
    y = 155
    for idx, (zone, title, nodes) in enumerate(zones):
        body.append(f'<rect x="58" y="{y}" width="1040" height="137" rx="18" fill="white" stroke="{accent}" stroke-width="2" filter="url(#shadow)"/>')
        body.append(f'<rect x="58" y="{y}" width="190" height="137" rx="18" fill="{accent}"/><text x="153" y="{y+53}" text-anchor="middle" font-size="25" font-weight="850" fill="white">{zone}</text><text x="153" y="{y+84}" text-anchor="middle" font-size="13" font-weight="800" fill="white">{svg_escape(title)}</text>')
        node_w = 246
        for node_idx, node in enumerate(nodes):
            x = 282 + node_idx * 268
            body.append(f'<rect x="{x}" y="{y+36}" width="{node_w}" height="67" rx="12" fill="#f4f8fd" stroke="#a9bfdc"/>')
            body.append(text_lines(x+node_w/2, y+64, node, 25, 16, "#17314f", 700, max_lines=2, line_height=18))
        y += 153
    body.append('<rect x="1130" y="155" width="412" height="596" rx="20" fill="#071b38" filter="url(#shadow)"/>')
    body.append(f'<text x="1170" y="205" font-size="22" font-weight="850" fill="{soft}">PUBLICATION &amp; RUNTIME CONTROLS</text>')
    controls = project["controls"][:4]
    for idx, control in enumerate(controls):
        cy = 245 + idx * 101
        body.append(f'<circle cx="1172" cy="{cy+19}" r="16" fill="{accent}"/><text x="1172" y="{cy+25}" text-anchor="middle" font-size="14" font-weight="850" fill="white">{idx+1}</text>')
        body.append(text_lines(1204, cy+12, control, 34, 17, "white", 700, anchor="start", max_lines=3, line_height=20))
    body.append(f'<rect x="1161" y="658" width="350" height="58" rx="12" fill="{accent}"/><text x="1336" y="693" text-anchor="middle" font-size="17" font-weight="850" fill="white">SECRETS &amp; CUSTOMER DATA EXCLUDED</text>')
    return svg_shell(project, "Trust boundaries, publication controls and risk paths", "".join(body), "Technical evidence is published without credentials, customer datasets, model weights, or live deployment state.")


def target_roadmap(project: dict) -> str:
    accent, soft = CATEGORY_COLORS.get(project["category"], CATEGORY_COLORS["Enterprise operations"])
    current = (project["components"]["services"] + project["components"]["ai"])[:4]
    harden = project["controls"][:4]
    scale = (project.get("roadmap") or project["skills"][:4])[:4]
    columns = [("CURRENT EVIDENCE", current), ("HARDEN & PRODUCTIZE", harden), ("SCALE & OPERATE", scale)]
    body = [f'<text x="70" y="177" font-size="20" font-weight="800" fill="{accent}">TARGET ARCHITECTURE AND DELIVERY ROADMAP</text>']
    for idx, (title, items) in enumerate(columns):
        x = 72 + idx * 505
        header_fill = accent if idx < 2 else "#071b38"
        header_text = "white" if idx < 2 else soft
        body.append(f'<rect x="{x}" y="220" width="455" height="510" rx="22" fill="white" stroke="#b7cae4" filter="url(#shadow)"/>')
        body.append(f'<rect x="{x}" y="220" width="455" height="78" rx="22" fill="{header_fill}"/><text x="{x+227}" y="267" text-anchor="middle" font-size="20" font-weight="850" fill="{header_text}">{svg_escape(title)}</text>')
        for item_idx, item in enumerate(items or ["Source evidence unavailable"]):
            y = 332 + item_idx * 88
            body.append(f'<circle cx="{x+52}" cy="{y+26}" r="18" fill="{soft}"/><text x="{x+52}" y="{y+32}" text-anchor="middle" font-size="15" font-weight="850" fill="#17314f">{item_idx+1}</text>')
            body.append(text_lines(x+88, y+17, item, 36, 17, "#17314f", 720, anchor="start", max_lines=3, line_height=20))
        if idx < 2:
            body.append(f'<line x1="{x+463}" y1="475" x2="{x+495}" y2="475" stroke="#173c78" stroke-width="4" marker-end="url(#arrow)"/>')
    return svg_shell(project, "Target architecture and roadmap", "".join(body), "Move from demonstrated capability to hardened controls, measurable operations, and repeatable scale.")


def build_architecture_pack(project: dict, architecture_dir: Path) -> list[str]:
    architecture_dir.mkdir(parents=True, exist_ok=True)
    diagrams = [
        ("01-executive-architecture.svg", architecture_overview(project)),
        ("02-runtime-data-flow.svg", runtime_flow(project)),
        ("03-system-context-deployment.svg", system_context(project)),
        ("04-authenticated-lifecycle.svg", authenticated_lifecycle(project)),
        ("05-data-architecture.svg", data_architecture(project)),
        ("06-workflow-orchestration.svg", workflow_architecture(project)),
        ("07-ai-control-plane.svg", ai_control_plane(project)),
        ("08-trust-boundaries.svg", trust_boundaries(project)),
        ("09-target-architecture-roadmap.svg", target_roadmap(project)),
    ]
    for filename, content in diagrams:
        write_text_lf(architecture_dir / filename, content)
    reference_files: list[str] = []
    if project["slug"] == "ideastorm" and REFERENCE_PACK.exists():
        ref_dir = architecture_dir / "reference-pack"
        thumbnail_dir = ref_dir / "thumbnails"
        ref_dir.mkdir(parents=True, exist_ok=True)
        thumbnail_dir.mkdir(parents=True, exist_ok=True)
        reference_bytes = 0
        reference_names: set[str] = set()
        with zipfile.ZipFile(REFERENCE_PACK) as zf:
            for info in zf.infolist():
                if info.is_dir() or not safe_entry(info.filename) or PurePosixPath(info.filename).suffix.lower() != ".png":
                    continue
                filename = PurePosixPath(info.filename).name
                if filename in reference_names or info.file_size > MAX_REFERENCE_PNG_BYTES:
                    raise RuntimeError(f"Unsafe or duplicate IdeaStorm reference image: {filename}")
                data = zf.read(info)
                if not data.startswith(b"\x89PNG\r\n\x1a\n"):
                    raise RuntimeError(f"Invalid PNG reference image: {filename}")
                reference_bytes += len(data)
                if reference_bytes > MAX_REFERENCE_TOTAL_BYTES:
                    raise RuntimeError("IdeaStorm reference image pack exceeds the public size cap")
                (ref_dir / filename).write_bytes(data)
                with Image.open(io.BytesIO(data)) as source_image:
                    source_image.thumbnail((960, 540), Image.Resampling.LANCZOS)
                    thumbnail = source_image.convert("RGB")
                    thumbnail.save(
                        thumbnail_dir / f"{Path(filename).stem}.webp",
                        format="WEBP",
                        quality=76,
                        method=6,
                    )
                reference_names.add(filename)
                reference_files.append(f"reference-pack/{filename}")
        if len(reference_files) != 9:
            raise RuntimeError(f"Expected 9 IdeaStorm reference images, found {len(reference_files)}")
    return [filename for filename, _ in diagrams] + sorted(reference_files)


def human_bytes(size: int) -> str:
    if size < 1_000:
        return f"{size} B"
    if size < 1_000_000:
        return f"{size / 1_000:.0f} KB"
    return f"{size / 1_000_000:.1f} MB"


def public_evidence_map(project: dict, manifest: dict) -> str:
    meaningful = [item for item in manifest["included_file_details"] if item["meaningful"]]

    def files_for(*role_fragments: str) -> str:
        matches = [
            item["file"] for item in meaningful
            if any(fragment.lower() in role.lower() for role in item["roles"] for fragment in role_fragments)
        ]
        matches = list(dict.fromkeys(matches))[:8]
        return ", ".join(f"`{name}`" for name in matches) or "Not established by a non-empty anonymized sample"

    decisions = project.get("decision_evidence") or []
    decision_claim = " ".join(decisions) if decisions else "Technical decision rationale not established from the supplied archive."
    rows = [
        ("System structure and runtime flow", files_for("Service", "Workflow", "Data")),
        ("AI or automation role", files_for("AI / retrieval", "Workflow")),
        ("Controls and validation", files_for("Control", "Test")),
        ("Delivery and operational seams", files_for("Operations", "Configuration")),
        ("Documented decision evidence", files_for("Control", "Workflow", "Data") if decisions else "Not established from the supplied archive"),
    ]
    table = "\n".join(f"| {claim} | {evidence} | Static code reading only |" for claim, evidence in rows)
    inventory = "\n".join(
        f"| `{item['file']}` | {'Meaningful sample' if item['meaningful'] else 'Retained empty placeholder'} | "
        f"{item['bytes']:,} | {', '.join(item['roles'])} |"
        for item in manifest["included_file_details"]
    ) or "| — | No source sample available | 0 | Documentation-only archive |"
    return f"""# Public evidence map — {project['name']}

This map connects public claim areas to anonymized samples. Original archive-member paths are intentionally not published. The source was reviewed statically and was not executed, deployed or runtime-verified.

## Evidence boundary

- Source evidence: **{manifest['non_empty_file_count']} meaningful anonymized samples**
- Retained empty placeholders: **{manifest['empty_file_count']}**
- Verification: **Static review only · code not executed**
- Delivery maturity: **{project['evidence_profile']['maturity']}**
- Intelligence type: **{project['evidence_profile']['intelligence']}**
- Ownership: **{project.get('ownership_evidence') or 'Personal ownership not established from the supplied archive.'}**
- Outcomes: **{project.get('outcome_evidence') or 'Measured business or runtime outcomes not established from the supplied archive.'}**
- Decision evidence: **{decision_claim}**

## Claim-to-sample map

| Public claim area | Anonymized published evidence | Verification boundary |
|---|---|---|
{table}

The map identifies evidence roles, not proof of production operation. A sample may support more than one claim area; absence of a mapped sample is shown explicitly rather than inferred.

## Published sample inventory

| Anonymized file | Evidence status | Bytes | Inferred review roles |
|---|---:|---:|---|
{inventory}
"""


def inline_excerpt(project: dict, package_path: Path, manifest: dict) -> dict | None:
    if not project.get("flagship"):
        return None
    allowed = {".py", ".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".java", ".cs", ".go", ".rs", ".sql"}
    candidates = []
    for index, item in enumerate(manifest["included_file_details"]):
        suffix = PurePosixPath(item["file"]).suffix.lower()
        if not item["meaningful"] or suffix not in allowed:
            continue
        role_score = sum(role in {"AI / retrieval", "Control / validation", "Workflow / orchestration", "Service / API"} for role in item["roles"])
        candidates.append((-role_score, index, item))
    if not candidates:
        return None
    _, _, chosen = sorted(candidates, key=lambda row: (row[0], row[1]))[0]
    with zipfile.ZipFile(package_path) as zf:
        text = zf.read(chosen["file"]).decode("utf-8")
    lines = text.splitlines()
    focus = 0
    focus_pattern = re.compile(r"^\s*(?:async\s+def|def|class|async\s+function|function|export\s+(?:async\s+)?(?:function|class|const)|(?:public|private|protected)?\s*(?:async\s+)?[A-Za-z_].*\{|@(?:app|router)\.)")
    for index, line in enumerate(lines):
        if focus_pattern.search(line):
            focus = max(0, index - 2)
            if lines[focus].lstrip().startswith(("*", "*/")):
                comment_start = next(
                    (candidate for candidate in range(index - 1, max(-1, index - 9), -1) if lines[candidate].lstrip().startswith(("/**", "/*"))),
                    None,
                )
                focus = comment_start if comment_start is not None else index
            break
    excerpt_lines = [line[:220].rstrip() for line in lines[focus:focus + 22]]
    while excerpt_lines and not excerpt_lines[-1].strip():
        excerpt_lines.pop()
    excerpt_text = "\n".join(excerpt_lines)
    if not excerpt_text.strip():
        return None
    language = {
        ".py": "python", ".js": "javascript", ".jsx": "jsx", ".mjs": "javascript",
        ".cjs": "javascript", ".ts": "typescript", ".tsx": "tsx", ".java": "java",
        ".cs": "csharp", ".go": "go", ".rs": "rust", ".sql": "sql",
    }.get(PurePosixPath(chosen["file"]).suffix.lower(), "text")
    return {"file": chosen["file"], "language": language, "text": excerpt_text, "roles": chosen["roles"]}


def image_dimensions(path: Path) -> tuple[int, int]:
    if path.suffix.lower() == ".svg":
        return 1600, 900
    data = path.read_bytes()[:24]
    if path.suffix.lower() == ".png" and data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        return struct.unpack(">II", data[16:24])
    return 1600, 900


def json_ld_script(payload: dict) -> str:
    value = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f'<script type="application/ld+json">{value}</script>'


def social_meta(*, title: str, description: str, canonical: str, schema: dict) -> str:
    title_attr = html.escape(title, quote=True)
    description_attr = html.escape(description, quote=True)
    canonical_attr = html.escape(canonical, quote=True)
    return (
        f'<link rel="canonical" href="{canonical_attr}">'
        f'<meta property="og:type" content="website"><meta property="og:site_name" content="Aditya Singh Portfolio">'
        f'<meta property="og:title" content="{title_attr}"><meta property="og:description" content="{description_attr}">'
        f'<meta property="og:url" content="{canonical_attr}"><meta property="og:image" content="{SOCIAL_IMAGE_URL}">'
        f'<meta property="og:image:alt" content="Aditya Singh enterprise AI and technical portfolio">'
        f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title_attr}">'
        f'<meta name="twitter:description" content="{description_attr}"><meta name="twitter:image" content="{SOCIAL_IMAGE_URL}">'
        f'{json_ld_script(schema)}'
    )


def project_readme(project: dict, package_manifest: dict) -> str:
    stack = " · ".join(project["stack"])
    skills = "\n".join(f"- {skill}" for skill in project["skills"])
    flow = " → ".join(project["flow"])
    status_note = (
        "The supplied archive did not contain an implementation. The architecture views are explicitly conceptual and make no source-verified implementation claim."
        if project["evidence_level"] == "concept"
        else "The technical claims below are grounded in the supplied source archive."
    )
    decisions = "\n".join(f"- {item}" for item in (project.get("decision_evidence") or []))
    return f"""# {project['name']}

- **Evidence status:** {project['evidence_label']}
- **Source evidence:** {project['evidence_profile']['source']}
- **Verification:** {project['evidence_profile']['verification']}
- **Delivery maturity:** {project['evidence_profile']['maturity']}
- **Intelligence type:** {project['evidence_profile']['intelligence']}
- **Category:** {project['category']}
- **Project family:** {project['family']}
- **Source package:** `{project['archive']}`

{project['summary']}

{status_note}

## AI or automation role

{project['ai_role']}

## Technical stack

{stack}

## Skills demonstrated

{skills}

## Primary system flow

{flow}

## Architecture image pack

- `architecture/01-executive-architecture.svg`
- `architecture/02-runtime-data-flow.svg`
- `architecture/03-system-context-deployment.svg`
- `architecture/04-authenticated-lifecycle.svg`
- `architecture/05-data-architecture.svg`
- `architecture/06-workflow-orchestration.svg`
- `architecture/07-ai-control-plane.svg`
- `architecture/08-trust-boundaries.svg`
- `architecture/09-target-architecture-roadmap.svg`

IdeaStorm additionally includes the nine supplied PNG reference diagrams under `architecture/reference-pack/`.

## Source evidence reviewed

See [`PUBLIC_EVIDENCE_MAP.md`](PUBLIC_EVIDENCE_MAP.md) for a claim-to-sample map and the complete anonymized sample inventory. Original archive-member paths are intentionally not published.

## Attribution, outcomes and decisions

- **Personal ownership:** {project.get('ownership_evidence') or 'Not established from the supplied archive.'}
- **Measured outcomes:** {project.get('outcome_evidence') or 'Not established from the supplied archive.'}

{decisions or '- **Technical decision rationale:** Not established from the supplied archive.'}

## Public-package boundary

This is a curated, non-runnable portfolio snapshot rather than the original production archive. Credentials, environment files, customer datasets, contract documents, employee records, database backups, vector indexes, model weights, generated dependencies, media and live deployment state are excluded. Selected source text is anonymized, scanned and redacted for credential-like values, known customer names, identity literals, email addresses, phone numbers, identifiers, service URLs, network addresses and local filesystem paths.

- Meaningful anonymized source samples: **{package_manifest['non_empty_file_count']}**
- Retained empty source placeholders: **{package_manifest['empty_file_count']}**
- Total included source files: **{package_manifest['included_file_count']}**
- Included sanitized source bytes: **{package_manifest['included_bytes']:,}**
"""


def security_notice(project: dict, manifest: dict) -> str:
    redacted_count = len(manifest["redacted_files"])
    return f"""# Security and redaction notice

This package was generated from `{project['archive']}` for public portfolio review.

- Project code was not executed during review or packaging.
- Only allow-listed text source and configuration files were considered.
- {redacted_count} included files required one or more automated redactions.
- Secrets, private keys, environment files, credentials, customer/employee datasets, contract files, databases, indexes, backups, model weights, media and generated dependencies were excluded.
- Known customer names, identity literals, email addresses, phone numbers, identifiers, service URLs, network addresses and local filesystem paths were neutralized where detected.
- The package is an architectural/code-reading sample, not a production deployment artifact.

The original archive should be handled as sensitive until every separately reported credential rotation is complete.
"""


def technical_library_readme(projects: list[dict], project_stats: dict[str, dict]) -> str:
    levels = Counter(project["evidence_level"] for project in projects)
    categories = Counter(project["category"] for project in projects)
    category_lines = "\n".join(f"- {name}: {count}" for name, count in sorted(categories.items()))
    rows = []
    for project in projects:
        stats = project_stats[project["slug"]]
        rows.append(
            f"| [{project['name']}]({project['slug']}/) | {project['evidence_label']} | "
            f"9 | {stats['non_empty_file_count']} | {stats['empty_file_count']} | [{stats['package_file']}]({project['slug']}/{stats['package_file']}) |"
        )
    return f"""# Technical project library

This public evidence library contains **{len(projects)}** source-reviewed technical briefs, **{len(projects) * 9}** newly generated architecture views, and **9** supplied IdeaStorm reference images.

Evidence classification:

- Code-derived implementations: {levels['implemented']}
- Source-backed prototypes: {levels['prototype']}
- Deterministic / AI-enabling systems: {levels['deterministic']}
- Documentation-only source: {levels['concept']}

## Capability groups

{category_lines}

## Public-package boundary

The downloadable packages are anonymized, non-runnable code-reading snapshots. They exclude credentials, environment files, customer and employee datasets, contract documents, databases, backups, vector indexes, model weights, generated dependencies, media and live deployment state. Source member paths are anonymized and sensitive literals are neutralized. Original project code was not executed during review or packaging.

## Project index

| Project | Evidence status | Architecture views | Meaningful samples | Retained empty placeholders | Package |
|---|---:|---:|---:|---:|---|
{chr(10).join(rows)}

Full package checksums are available in `SHA256SUMS.txt` and `build-manifest.json`.
"""


def verify_public_zip(zip_path: Path) -> None:
    if zip_path.stat().st_size >= MAX_PUBLIC_ZIP_BYTES:
        raise RuntimeError(f"Public package exceeds GitHub's safe per-file limit: {zip_path}")
    with zipfile.ZipFile(zip_path) as zf:
        bad = zf.testzip()
        if bad:
            raise RuntimeError(f"CRC failure in {zip_path}: {bad}")
        names: set[str] = set()
        total_uncompressed = 0
        for info in zf.infolist():
            if not safe_entry(info.filename) or is_symlink(info) or info.filename in names:
                raise RuntimeError(f"Unsafe or duplicate public ZIP member: {zip_path}:{info.filename}")
            names.add(info.filename)
            total_uncompressed += info.file_size
            if total_uncompressed > 50_000_000:
                raise RuntimeError(f"Public ZIP has an excessive uncompressed payload: {zip_path}")
            if info.is_dir():
                continue
            data = zf.read(info)
            if info.filename.lower().endswith(".png"):
                if not data.startswith(b"\x89PNG\r\n\x1a\n"):
                    raise RuntimeError(f"Invalid PNG remained in {zip_path}:{info.filename}")
                continue
            if info.filename.lower().endswith(".webp"):
                if len(data) < 12 or not data.startswith(b"RIFF") or data[8:12] != b"WEBP":
                    raise RuntimeError(f"Invalid WebP remained in {zip_path}:{info.filename}")
                continue
            text = decode_text(data)
            if text is None:
                raise RuntimeError(f"Unexpected non-text file remained in {zip_path}:{info.filename}")
            findings = unresolved_sensitive_findings(text, include_opaque=info.filename.startswith("source/"))
            if findings:
                raise RuntimeError(f"Sensitive content remained in {zip_path}:{info.filename}: {', '.join(findings)}")


def build_package(project: dict, project_dir: Path, architecture_files: list[str]) -> dict:
    stage = ensure_within(BUILD_ROOT / project["slug"], BUILD_ROOT)
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)
    manifest = select_and_sanitize_source(project, stage / "source")
    write_text_lf(stage / "README.md", project_readme(project, manifest))
    write_text_lf(stage / "PUBLIC_EVIDENCE_MAP.md", public_evidence_map(project, manifest))
    write_text_lf(stage / "SECURITY_AND_REDACTION.md", security_notice(project, manifest))
    shutil.copytree(project_dir / "architecture", stage / "architecture")
    manifest["architecture_files"] = architecture_files
    write_text_lf(stage / "SOURCE_MANIFEST.json", json.dumps(manifest, indent=2))
    zip_path = project_dir / f"{project['slug']}-portfolio-source.zip"
    temp_zip = project_dir / f".{project['slug']}-portfolio-source.zip.tmp"
    if temp_zip.exists():
        temp_zip.unlink()
    with zipfile.ZipFile(temp_zip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as out_zip:
        for file in sorted(stage.rglob("*")):
            if file.is_file():
                archive_name = file.relative_to(stage).as_posix()
                entry = zipfile.ZipInfo(archive_name, date_time=(1980, 1, 1, 0, 0, 0))
                entry.compress_type = zipfile.ZIP_DEFLATED
                entry.external_attr = 0o100644 << 16
                entry.create_system = 3
                out_zip.writestr(entry, file.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    verify_public_zip(temp_zip)
    temp_zip.replace(zip_path)
    manifest["package_file"] = zip_path.name
    manifest["package_bytes"] = zip_path.stat().st_size
    manifest["package_sha256"] = sha256_file(zip_path)
    shutil.rmtree(stage)
    return manifest


def status_class(level: str) -> str:
    return {"implemented": "implemented", "prototype": "prototype", "deterministic": "deterministic", "concept": "concept"}.get(level, "prototype")


def evidence_badges(project: dict, package: dict) -> str:
    source_value = (
        f"{package['non_empty_file_count']} meaningful sample{'s' if package['non_empty_file_count'] != 1 else ''}"
        if package["non_empty_file_count"]
        else project["evidence_profile"]["source"]
    )
    dimensions = (
        ("Source", source_value),
        ("Verification", project["evidence_profile"]["verification"]),
        ("Maturity", project["evidence_profile"]["maturity"]),
        ("Intelligence", project["evidence_profile"]["intelligence"]),
    )
    return '<div class="evidence-dimensions" aria-label="Independent evidence profile">' + "".join(
        f'<span><small>{html.escape(label)}</small>{html.escape(value)}</span>' for label, value in dimensions
    ) + "</div>"


def project_card(project: dict, package: dict, *, searchable: bool) -> str:
    stack = "".join(f"<span>{html.escape(item)}</span>" for item in project["stack"][:5])
    search = " ".join([
        project["name"], project["category"], project["capability"], project["family"], project["summary"],
        project["evidence_profile"]["intelligence"], *project["stack"], *project["skills"],
    ]).lower()
    attributes = ""
    if searchable:
        attributes = (
            f' data-project-card data-name="{html.escape(project["name"].lower(), quote=True)}"'
            f' data-capability="{html.escape(project["capability"], quote=True)}"'
            f' data-status="{html.escape(project["evidence_level"], quote=True)}"'
            f' data-family="{html.escape(project["family"], quote=True)}"'
            f' data-search="{html.escape(search, quote=True)}"'
        )
    empty_note = f" · {package['empty_file_count']} empty retained" if package["empty_file_count"] else ""
    package_cta = "Evidence-gap pack ↓" if project["evidence_level"] == "concept" else "Source package ↓"
    return f'''<article class="tech-project-card"{attributes}>
<a class="tech-project-visual" href="samples/technical-projects/{project['slug']}/index.html"><img src="samples/technical-projects/{project['slug']}/architecture/01-executive-architecture.svg" alt="{html.escape(project['name'])} technical architecture overview" width="1600" height="900" loading="lazy" decoding="async"></a>
<div class="tech-project-body"><div class="tech-project-meta"><span>{html.escape(project['category'])}</span><strong class="evidence-status {status_class(project['evidence_level'])}">{html.escape(project['evidence_label'])}</strong></div><h3>{html.escape(project['name'])}</h3><p>{html.escape(project['summary'])}</p><div class="tech-stack-list">{stack}</div>{evidence_badges(project, package)}<div class="tech-card-evidence"><span>09 architecture views</span><span>{package['non_empty_file_count']:02d} meaningful samples{html.escape(empty_note)}</span><span>{html.escape(project['family'])}</span></div><div class="tech-project-actions"><a href="samples/technical-projects/{project['slug']}/index.html">Technical brief →</a><a href="samples/technical-projects/{project['slug']}/{project['slug']}-portfolio-source.zip">{package_cta}</a></div></div></article>'''


def select_options(values: list[str], first_label: str) -> str:
    return f'<option value="all">{html.escape(first_label)}</option>' + "".join(
        f'<option value="{html.escape(value, quote=True)}">{html.escape(value)}</option>' for value in values
    )


def technical_index_page(projects: list[dict], build_stats: dict) -> str:
    flagships = [project for project in projects if project.get("flagship")]
    concepts = [project for project in projects if project["evidence_level"] == "concept"]
    flagship_cards = "".join(project_card(project, build_stats[project["slug"]], searchable=False) for project in flagships)
    library_cards = "".join(project_card(project, build_stats[project["slug"]], searchable=True) for project in projects)
    capabilities = sorted({project["capability"] for project in projects})
    families = sorted({project["family"] for project in projects})
    maturity_options = [
        ("implemented", "Implementation archives"),
        ("prototype", "Prototype archives"),
        ("deterministic", "Deterministic implementations"),
        ("concept", "Concepts / evidence gaps"),
    ]
    statuses = '<option value="all">All evidence statuses</option>' + "".join(
        f'<option value="{value}">{label}</option>' for value, label in maturity_options
    )
    meaningful_total = sum(stats["non_empty_file_count"] for stats in build_stats.values())
    canonical = f"{SITE_BASE}/technical-projects.html"
    title = "Technical Systems & AI Portfolio — Aditya Singh"
    description = f"A recruiter-first path through 8 flagship systems and a complete evidence library of {len(projects)} technical projects."
    schema = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": title,
        "description": description,
        "url": canonical,
        "author": {"@type": "Person", "name": "Aditya Singh", "url": SITE_BASE + "/"},
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(projects),
            "itemListElement": [
                {"@type": "ListItem", "position": index, "url": f"{SITE_BASE}/samples/technical-projects/{project['slug']}/", "name": project["name"]}
                for index, project in enumerate(projects, 1)
            ],
        },
    }
    meta = social_meta(title=title, description=description, canonical=canonical, schema=schema)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><meta name="description" content="{html.escape(description, quote=True)}">{meta}<link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="technical-projects.css"></head><body class="technical-page"><a class="skip-link" href="#main">Skip to content</a><header class="site-header"><a class="brand" href="index.html"><span class="brand-mark">AS</span><span class="brand-copy"><strong>Aditya Singh</strong><small>Technical systems &amp; AI</small></span></a><nav class="site-nav" aria-label="Technical library navigation"><a href="#flagships">Flagships</a><a href="#complete-library">All 38</a><a href="technical-concepts.html">Concepts</a><a href="#method">Evidence method</a></nav><a class="header-cta" href="mailto:{CONTACT_EMAIL}?subject=Technical%20portfolio%20discussion">Discuss ↗</a></header><main id="main"><section class="technical-hero"><div><p class="eyebrow light"><span></span> Recruiter-first technical portfolio</p><h1>Eight flagship systems.<br><em>All evidence preserved.</em></h1><p>Start with the strongest source-backed systems, then open the complete {len(projects)}-project library or the clearly labelled concepts and target-state collection. No project, diagram, reference image or source package has been removed.</p><div class="project-hero-actions"><a class="button button-accent" href="#flagships">Review flagships ↓</a><a class="button button-light" href="#complete-library">Open all {len(projects)} →</a></div></div><div class="technical-proof"><div><strong>{len(flagships):02d}</strong><span>flagship systems</span></div><div><strong>{len(projects):02d}</strong><span>complete briefs</span></div><div><strong>{meaningful_total:03d}</strong><span>meaningful samples</span></div><div><strong>{concepts.__len__():02d}</strong><span>preserved concepts</span></div></div></section><section class="technical-boundary" id="method"><strong>Evidence boundary</strong><p>Every project separates source evidence, static verification, delivery maturity and intelligence type. Code was reviewed but not executed. Empty source placeholders remain in packages for completeness but are not counted as meaningful evidence.</p></section><section class="technical-routes section" aria-labelledby="routes-title"><div class="section-heading"><p class="eyebrow"><span></span> Choose a review path</p><h2 id="routes-title">Depth without losing the archive.</h2></div><div class="technical-route-grid"><a href="#flagships"><strong>Flagship review</strong><span>Eight strongest systems, surfaced first.</span></a><a href="#complete-library"><strong>Complete library</strong><span>All {len(projects)} projects with capability, status and family filters.</span></a><a href="technical-concepts.html"><strong>Concepts &amp; target states</strong><span>All {len(concepts)} source-incomplete archives, preserved with evidence-gap labels.</span></a></div></section><section class="technical-library section" id="flagships"><div class="section-heading split-heading"><div><p class="eyebrow"><span></span> Flagship systems</p><h2>Eight briefs to review first.</h2></div><p>Selected for architecture depth, control design and meaningful sanitized source evidence. Selection is editorial, not a production-runtime claim.</p></div><div class="tech-project-grid flagship-grid">{flagship_cards}</div></section><section class="technical-library complete-library section" id="complete-library"><div class="section-heading split-heading"><div><p class="eyebrow"><span></span> Complete technical library</p><h2>All {len(projects)} projects remain discoverable.</h2></div><p>Open the library, then search by technology or filter independently by capability, evidence status and project family.</p></div><details class="library-disclosure" data-complete-library><summary><span>Open the complete project library</span><strong>{len(projects)} briefs · {len(projects) * 9} generated architecture views</strong></summary><div class="library-disclosure-body"><div class="tech-tools"><label class="tech-search"><span>Search</span><input type="search" placeholder="RAG, agents, FastAPI, PostgreSQL, Playwright…" data-tech-search></label><label><span>Capability</span><select data-tech-capability>{select_options(capabilities, 'All capabilities')}</select></label><label><span>Evidence status</span><select data-tech-status>{statuses}</select></label><label><span>Project family</span><select data-tech-family>{select_options(families, 'All project families')}</select></label><label><span>Order</span><select data-tech-sort><option value="featured">Portfolio order</option><option value="az">Name A–Z</option></select></label><button type="button" data-tech-clear>Clear filters</button><span data-tech-count>{len(projects)} projects</span></div><div class="tech-project-grid" data-tech-grid>{library_cards}</div><p class="tech-empty" data-tech-empty hidden>No projects match that search and filter combination.</p></div></details></section></main><footer class="site-footer"><span>© Aditya Singh · Technical project evidence</span><div><a href="technical-concepts.html">Concepts &amp; target states</a><a href="index.html">Return to portfolio ↑</a></div></footer><script src="technical-projects.js"></script></body></html>'''


def technical_concepts_page(projects: list[dict], build_stats: dict) -> str:
    concepts = [project for project in projects if project["evidence_level"] == "concept"]
    cards = "".join(project_card(project, build_stats[project["slug"]], searchable=False) for project in concepts)
    canonical = f"{SITE_BASE}/technical-concepts.html"
    title = "Concepts & Target-State Designs — Aditya Singh"
    description = f"All {len(concepts)} source-incomplete technical concepts preserved with explicit evidence gaps, architecture views and downloadable review packs."
    schema = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": title,
        "description": description,
        "url": canonical,
        "author": {"@type": "Person", "name": "Aditya Singh", "url": SITE_BASE + "/"},
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(concepts),
            "itemListElement": [
                {"@type": "ListItem", "position": index, "url": f"{SITE_BASE}/samples/technical-projects/{project['slug']}/", "name": project["name"]}
                for index, project in enumerate(concepts, 1)
            ],
        },
    }
    meta = social_meta(title=title, description=description, canonical=canonical, schema=schema)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><meta name="description" content="{html.escape(description, quote=True)}">{meta}<link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="technical-projects.css"></head><body class="technical-page concepts-page"><a class="skip-link" href="#main">Skip to content</a><header class="site-header"><a class="brand" href="index.html"><span class="brand-mark">AS</span><span class="brand-copy"><strong>Aditya Singh</strong><small>Concepts &amp; target states</small></span></a><nav class="site-nav" aria-label="Concept library navigation"><a href="technical-projects.html#flagships">Flagships</a><a href="technical-projects.html#complete-library">All projects</a><a href="#concepts">Concepts</a></nav><a class="header-cta" href="technical-projects.html">Technical library ↗</a></header><main id="main"><section class="technical-hero concept-hero"><div><p class="eyebrow light"><span></span> Preserved with explicit boundaries</p><h1>{len(concepts)} concepts.<br><em>No invented evidence.</em></h1><p>These archives remain part of the portfolio. Their supplied sources did not establish an implementation, so each brief preserves its target-state architecture while making the evidence gap unmistakable.</p><a class="button button-accent" href="#concepts">Review the concepts ↓</a></div><div class="technical-proof"><div><strong>{len(concepts):02d}</strong><span>concept briefs</span></div><div><strong>{len(concepts) * 9:02d}</strong><span>architecture views</span></div><div><strong>00</strong><span>meaningful samples</span></div><div><strong>01</strong><span>clear route back</span></div></div></section><section class="technical-boundary"><strong>Evidence-gap policy</strong><p>Conceptual architecture is retained as design material. It is not presented as implemented, deployed, tested or personally owned. Download actions are labelled evidence-gap packs rather than source packages.</p></section><section class="technical-library section" id="concepts"><div class="section-heading split-heading"><div><p class="eyebrow"><span></span> Concepts &amp; target states</p><h2>Every source-incomplete archive.</h2></div><p>Each brief preserves all nine generated views and the complete downloadable pack while explicitly recording what the supplied archive did not establish.</p></div><div class="tech-project-grid">{cards}</div></section></main><footer class="site-footer"><span>Concepts preserved · implementation claims withheld</span><a href="technical-projects.html">Complete technical library ↑</a></footer></body></html>'''


def project_detail_page(project: dict, package: dict, architecture_files: list[str], project_dir: Path, projects: list[dict]) -> str:
    stack = "".join(f"<span>{html.escape(item)}</span>" for item in project["stack"])
    skills = "".join(f"<li>{html.escape(item)}</li>" for item in project["skills"])
    controls = "".join(f"<li>{html.escape(item)}</li>" for item in project["controls"])
    sample_inventory = "".join(
        f'<li><code>{html.escape(item["file"])}</code><span>{"Meaningful sample" if item["meaningful"] else "Retained empty placeholder"} · {human_bytes(item["bytes"])}</span></li>'
        for item in package["included_file_details"]
    ) or "<li><span>No implementation source sample was available in the supplied archive.</span></li>"
    generated = [filename for filename in architecture_files if not filename.startswith("reference-pack/")]

    def diagram_link(filename: str, *, eager: bool = False) -> str:
        label = filename.replace(".svg", "").split("-", 1)[-1].replace("-", " ").title()
        return f'<a href="architecture/{html.escape(filename)}" target="_blank" rel="noopener"><img src="architecture/{html.escape(filename)}" alt="{html.escape(project["name"])} {html.escape(label)}" width="1600" height="900" loading="{"eager" if eager else "lazy"}" decoding="async"><span>{html.escape(label)} ↗</span></a>'

    primary_diagram = diagram_link(generated[0], eager=True)
    layered_diagrams = "".join(diagram_link(filename) for filename in generated[1:])
    references = [filename for filename in architecture_files if filename.startswith("reference-pack/")]
    reference_gallery = ""
    if references:
        items = []
        for index, filename in enumerate(references, 1):
            original_path = project_dir / "architecture" / filename
            thumbnail_rel = f"reference-pack/thumbnails/{Path(filename).stem}.webp"
            thumbnail_path = project_dir / "architecture" / thumbnail_rel
            image_file = thumbnail_rel if thumbnail_path.exists() else filename
            width, height = image_dimensions(thumbnail_path if thumbnail_path.exists() else original_path)
            items.append(f'<a href="architecture/{html.escape(filename)}" target="_blank" rel="noopener"><img src="architecture/{html.escape(image_file)}" alt="IdeaStorm supplied architecture reference {index}" width="{width}" height="{height}" loading="lazy" decoding="async"><span>Original reference view {index:02d} ↗</span></a>')
        reference_gallery = f'<section class="project-reference section"><div class="section-heading split-heading"><div><p class="eyebrow"><span></span> Supplied IdeaStorm image pack</p><h2>Nine original reference diagrams.</h2></div><p>Lightweight WebP previews are shown here; every link opens the original full-resolution PNG, and all originals remain in the downloadable package.</p></div><details class="architecture-layer"><summary>Open all nine supplied references</summary><div class="reference-gallery">{"".join(items)}</div></details></section>'

    flow = "".join(f"<li><span>{idx:02d}</span>{html.escape(item)}</li>" for idx, item in enumerate(project["flow"], 1))
    decisions = project.get("decision_evidence") or []
    decision_body = "".join(f"<li>{html.escape(item)}</li>" for item in decisions) if decisions else "<li>Technical decision rationale not established from the supplied archive.</li>"
    excerpt = inline_excerpt(project, project_dir / package["package_file"], package)
    excerpt_section = ""
    if excerpt:
        excerpt_section = f'''<section class="project-code section" id="code"><div class="section-heading split-heading"><div><p class="eyebrow"><span></span> Inline sanitized evidence</p><h2>A code sample before the download.</h2></div><p>Excerpted from <code>{html.escape(excerpt['file'])}</code> inside the already-sanitized public ZIP. Static review only; the code was not executed.</p></div><div class="code-sample"><div><strong>{html.escape(excerpt['file'])}</strong><span>{html.escape(' · '.join(excerpt['roles']))}</span></div><pre><code class="language-{html.escape(excerpt['language'])}">{html.escape(excerpt['text'])}</code></pre></div></section>'''

    related_pool = [
        candidate for candidate in projects
        if candidate["slug"] != project["slug"]
        and ((project["evidence_level"] == "concept") == (candidate["evidence_level"] == "concept"))
    ]
    related_candidates = [candidate for candidate in related_pool if candidate["family"] == project["family"]]
    if len(related_candidates) < 3:
        related_candidates.extend(
            candidate for candidate in related_pool
            if candidate not in related_candidates and candidate["capability"] == project["capability"]
        )
    if len(related_candidates) < 3:
        related_candidates.extend(candidate for candidate in related_pool if candidate not in related_candidates)
    related = related_candidates[:3]
    related_cards = "".join(
        f'<article><span>{html.escape(candidate["family"])}</span><h3>{html.escape(candidate["name"])}</h3><p>{html.escape(candidate["summary"])}</p><a href="../{candidate["slug"]}/index.html">Review related brief →</a></article>'
        for candidate in related
    )
    package_cta = "Download evidence-gap pack ↓" if project["evidence_level"] == "concept" else "Download sanitized source ↓"
    header_cta = "Evidence-gap pack ↓" if project["evidence_level"] == "concept" else "Source package ↓"
    subject = quote(f"Architecture discussion: {project['name']}")
    canonical = f"{SITE_BASE}/samples/technical-projects/{project['slug']}/"
    title = f"{project['name']} — Technical Brief"
    schema_type = "TechArticle" if project["evidence_level"] == "concept" else "SoftwareSourceCode"
    schema = {
        "@context": "https://schema.org",
        "@type": schema_type,
        "name": project["name"],
        "headline": project["name"],
        "description": project["summary"],
        "url": canonical,
        "image": SOCIAL_IMAGE_URL,
        "author": {"@type": "Person", "name": "Aditya Singh", "url": SITE_BASE + "/"},
        "keywords": project["skills"],
        "creativeWorkStatus": project["evidence_profile"]["maturity"],
    }
    if schema_type == "SoftwareSourceCode":
        schema["programmingLanguage"] = project["stack"]
        schema["codeSampleType"] = "sanitized static-review sample"
    meta = social_meta(title=title, description=project["summary"], canonical=canonical, schema=schema)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><meta name="description" content="{html.escape(project['summary'], quote=True)}">{meta}<link rel="icon" href="../../../favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="../../../styles.css"><link rel="stylesheet" href="../../../technical-projects.css"></head><body class="project-detail-page"><a class="skip-link" href="#main">Skip to content</a><header class="site-header"><a class="brand" href="../../../index.html"><span class="brand-mark">AS</span><span class="brand-copy"><strong>Aditya Singh</strong><small>Technical brief</small></span></a><nav class="site-nav" aria-label="Technical brief navigation"><a href="../../../technical-projects.html#complete-library">All projects</a><a href="#architecture">Architecture</a><a href="#evidence">Evidence</a><a href="#related">Related</a></nav><a class="header-cta" href="{project['slug']}-portfolio-source.zip">{header_cta}</a></header><main id="main"><section class="project-hero"><div><p class="eyebrow light"><span></span> {html.escape(project['category'])}</p><strong class="evidence-status {status_class(project['evidence_level'])}">{html.escape(project['evidence_label'])}</strong><h1>{html.escape(project['name'])}</h1><p>{html.escape(project['summary'])}</p><div class="project-hero-actions"><a class="button button-accent" href="{project['slug']}-portfolio-source.zip">{package_cta}</a><a class="button button-light" href="#architecture">View architecture ↓</a><a class="button button-light" href="mailto:{CONTACT_EMAIL}?subject={subject}">Discuss this architecture ↗</a></div></div><img src="architecture/01-executive-architecture.svg" alt="{html.escape(project['name'])} architecture overview" width="1600" height="900" fetchpriority="high" decoding="async"></section><section class="project-evidence-strip">{evidence_badges(project, package)}</section><section class="project-facts"><div><strong>AI / automation role</strong><p>{html.escape(project['ai_role'])}</p></div><div><strong>Technical stack</strong><div class="tech-stack-list">{stack}</div></div><div><strong>Package evidence</strong><p>{package['non_empty_file_count']} meaningful samples{f' · {package["empty_file_count"]} empty retained' if package['empty_file_count'] else ''}<br>{human_bytes(package['package_bytes'])} ZIP · <a href="PUBLIC_EVIDENCE_MAP.md">public evidence map</a><br><code>SHA-256 {package['package_sha256'][:16]}…</code></p></div></section><section class="project-narrative section"><div><p class="eyebrow"><span></span> Engineering evidence</p><h2>What the source demonstrates.</h2><ul class="skill-evidence-list">{skills}</ul></div><div><p class="eyebrow"><span></span> Primary flow</p><ol class="project-flow">{flow}</ol></div></section><section class="project-claims section" aria-labelledby="claims-title"><div class="section-heading"><p class="eyebrow"><span></span> Attribution and proof boundary</p><h2 id="claims-title">What the archive does—and does not—establish.</h2></div><div class="project-claim-grid"><article><h3>Personal ownership</h3><p>{html.escape(project.get('ownership_evidence') or 'Not established from the supplied archive.')}</p></article><article><h3>Measured outcomes</h3><p>{html.escape(project.get('outcome_evidence') or 'Not established from the supplied archive.')}</p></article><article><h3>Technical decisions</h3><ul>{decision_body}</ul></article></div></section>{excerpt_section}<section class="project-architecture section" id="architecture"><div class="section-heading split-heading"><div><p class="eyebrow"><span></span> Architecture image pack</p><h2>One primary view, eight deeper layers.</h2></div><p>The executive architecture is surfaced first. Open the remaining runtime, context, lifecycle, data, workflow, AI-control, trust and roadmap views when deeper review is useful. All nine remain embedded in the ZIP.</p></div><div class="architecture-primary">{primary_diagram}</div><details class="architecture-layer"><summary>Open the remaining eight architecture views</summary><div class="architecture-gallery">{layered_diagrams}</div></details></section>{reference_gallery}<section class="project-evidence section" id="evidence"><div><p class="eyebrow"><span></span> Anonymized source evidence</p><h2>Published sample inventory.</h2><p class="evidence-map-link"><a href="PUBLIC_EVIDENCE_MAP.md">Open the public claim-to-sample evidence map →</a></p><ul class="sample-inventory">{sample_inventory}</ul></div><div><p class="eyebrow"><span></span> Public controls</p><h2>What was removed or neutralized.</h2><ul>{controls}<li>Credentials and customer/employee datasets excluded</li><li>Identity literals, emails, phone numbers, IDs, service URLs and local paths neutralized</li><li>Models, indexes, backups, media and generated dependencies omitted</li></ul></div></section><section class="project-related section" id="related"><div class="section-heading split-heading"><div><p class="eyebrow"><span></span> Continue the review</p><h2>Related technical briefs.</h2></div><a class="button button-dark" href="mailto:{CONTACT_EMAIL}?subject={subject}">Discuss this architecture ↗</a></div><div class="related-project-grid">{related_cards}</div></section></main><footer class="site-footer"><span>Source reviewed without executing project code.</span><div><a href="../../../technical-concepts.html">Concepts &amp; target states</a><a href="../../../technical-projects.html#complete-library">All technical projects ↑</a></div></footer></body></html>'''


class GeneratedHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.duplicate_ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if key != "id" or not value:
                continue
            if value in self.ids:
                self.duplicate_ids.add(value)
            self.ids.add(value)


def validate_generated_site(public_out: Path, index_path: Path, concepts_path: Path, projects: list[dict]) -> None:
    expected_slugs = {project["slug"] for project in projects}
    actual_slugs = {path.name for path in public_out.iterdir() if path.is_dir()}
    if actual_slugs != expected_slugs:
        raise RuntimeError(f"Generated project directories differ from catalog: {actual_slugs ^ expected_slugs}")
    if index_path.read_text(encoding="utf-8").count("data-project-card") != len(projects):
        raise RuntimeError("Technical index card count does not match the catalog")
    concept_count = sum(project["evidence_level"] == "concept" for project in projects)
    if concepts_path.read_text(encoding="utf-8").count('class="tech-project-card"') != concept_count:
        raise RuntimeError("Concept-library card count does not match the catalog")
    projects_payload = json.loads((public_out / "projects.json").read_text(encoding="utf-8"))
    build_payload = json.loads((public_out / "build-manifest.json").read_text(encoding="utf-8"))
    if len(projects_payload.get("projects", [])) != len(projects) or set(build_payload) != expected_slugs:
        raise RuntimeError("Generated JSON manifests do not match the catalog")
    checksum_lines = (public_out / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines()
    if len(checksum_lines) != len(projects):
        raise RuntimeError("Generated checksum inventory does not match the catalog")

    html_files = [index_path, concepts_path, *sorted(public_out.glob("*/index.html"))]
    for page in html_files:
        page_text = page.read_text(encoding="utf-8")
        parser = GeneratedHTMLParser()
        parser.feed(page_text)
        parser.close()
        if parser.duplicate_ids:
            raise RuntimeError(f"Duplicate HTML ids in {page}: {sorted(parser.duplicate_ids)}")
        for marker in ('rel="canonical"', 'property="og:title"', 'property="og:image"', 'name="twitter:card"', 'type="application/ld+json"'):
            if marker not in page_text:
                raise RuntimeError(f"Missing social/structured metadata {marker} in {page}")

    for project in projects:
        project_dir = public_out / project["slug"]
        svgs = sorted((project_dir / "architecture").glob("*.svg"))
        if len(svgs) != 9:
            raise RuntimeError(f"Expected 9 generated SVGs for {project['slug']}, found {len(svgs)}")
        for svg in svgs:
            root = ElementTree.parse(svg).getroot()
            if not root.tag.endswith("svg") or root.attrib.get("viewBox") != "0 0 1600 900":
                raise RuntimeError(f"Invalid architecture SVG: {svg}")
        package = project_dir / f"{project['slug']}-portfolio-source.zip"
        verify_public_zip(package)
        evidence_map = project_dir / "PUBLIC_EVIDENCE_MAP.md"
        if not evidence_map.is_file() or "Original archive-member paths are intentionally not published" not in evidence_map.read_text(encoding="utf-8"):
            raise RuntimeError(f"Missing or unsafe public evidence map for {project['slug']}")
        with zipfile.ZipFile(package) as zf:
            if "PUBLIC_EVIDENCE_MAP.md" not in zf.namelist():
                raise RuntimeError(f"Evidence map missing from public package: {package}")
        detail = project_dir / "index.html"
        detail_text = detail.read_text(encoding="utf-8")
        required_refs = [package.name, *[f"architecture/{svg.name}" for svg in svgs]]
        for reference in required_refs:
            if reference not in detail_text:
                raise RuntimeError(f"Missing detail-page reference {reference} in {detail}")
        if project["slug"] == "ideastorm":
            thumbnails = sorted((project_dir / "architecture" / "reference-pack" / "thumbnails").glob("*.webp"))
            if len(thumbnails) != 9:
                raise RuntimeError(f"Expected 9 IdeaStorm reference thumbnails, found {len(thumbnails)}")

    for path in public_out.rglob("*"):
        if path.is_symlink():
            raise RuntimeError(f"Generated public tree contains a symlink: {path}")
        if path.is_file() and path.stat().st_size >= 100_000_000:
            raise RuntimeError(f"Generated public file exceeds GitHub's limit: {path}")


def main() -> None:
    projects = PROJECTS
    validate_catalog(projects)
    for temporary in (BUILD_ROOT, PUBLIC_BUILD_ROOT):
        ensure_within(temporary, ROOT)
        if temporary.exists():
            shutil.rmtree(temporary)
    BUILD_ROOT.mkdir()
    public_out = PUBLIC_BUILD_ROOT / "technical-projects"
    public_out.mkdir(parents=True)
    index_path = PUBLIC_BUILD_ROOT / "technical-projects.html"
    concepts_path = PUBLIC_BUILD_ROOT / "technical-concepts.html"
    project_stats: dict[str, dict] = {}
    try:
        write_text_lf(public_out / "projects.json", json.dumps({"projects": projects}, indent=2))
        for project in projects:
            project_dir = ensure_within(public_out / project["slug"], public_out)
            project_dir.mkdir()
            architecture_files = build_architecture_pack(project, project_dir / "architecture")
            package = build_package(project, project_dir, architecture_files)
            write_text_lf(project_dir / "README.md", project_readme(project, package))
            write_text_lf(project_dir / "PUBLIC_EVIDENCE_MAP.md", public_evidence_map(project, package))
            write_text_lf(project_dir / "index.html", project_detail_page(project, package, architecture_files, project_dir, projects))
            project_stats[project["slug"]] = package
        write_text_lf(public_out / "build-manifest.json", json.dumps(project_stats, indent=2))
        write_text_lf(public_out / "README.md", technical_library_readme(projects, project_stats))
        checksum_lines = [
            f"{stats['package_sha256']}  {slug}/{stats['package_file']}"
            for slug, stats in sorted(project_stats.items())
        ]
        write_text_lf(public_out / "SHA256SUMS.txt", "\n".join(checksum_lines) + "\n")
        write_text_lf(index_path, technical_index_page(projects, project_stats))
        write_text_lf(concepts_path, technical_concepts_page(projects, project_stats))
        validate_generated_site(public_out, index_path, concepts_path, projects)

        backup = ROOT / ".tmp-technical-projects-previous"
        ensure_within(backup, ROOT)
        if backup.exists():
            shutil.rmtree(backup)
        if OUT_ROOT.exists():
            OUT_ROOT.rename(backup)
        try:
            OUT_ROOT.parent.mkdir(parents=True, exist_ok=True)
            public_out.rename(OUT_ROOT)
            index_path.replace(ROOT / "technical-projects.html")
            concepts_path.replace(ROOT / "technical-concepts.html")
        except Exception:
            if OUT_ROOT.exists():
                shutil.rmtree(OUT_ROOT)
            if backup.exists():
                backup.rename(OUT_ROOT)
            raise
        if backup.exists():
            shutil.rmtree(backup)
    finally:
        if BUILD_ROOT.exists():
            shutil.rmtree(BUILD_ROOT)
        if PUBLIC_BUILD_ROOT.exists():
            shutil.rmtree(PUBLIC_BUILD_ROOT)
    print(json.dumps({
        "projects": len(projects),
        "architecture_files": sum(len(stats["architecture_files"]) for stats in project_stats.values()),
        "included_source_files": sum(stats["included_file_count"] for stats in project_stats.values()),
        "package_bytes": sum(stats["package_bytes"] for stats in project_stats.values()),
        "largest_package": max((stats["package_bytes"], slug) for slug, stats in project_stats.items()),
    }, indent=2))


if __name__ == "__main__":
    main()
