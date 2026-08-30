#!/usr/bin/env python3
"""Dependency-free structural, accessibility, metadata and link QA.

The checker validates public HTML pages only: root pages and any other page
whose canonical URL belongs to the deployed portfolio. It never requests a
network resource or executes project code.
"""

from __future__ import annotations

import argparse
import json
import re
import struct
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
SITE_ORIGIN = "https://singhaditya21.github.io"
SITE_PREFIX = "/Resume/"
SITE_BASE = SITE_ORIGIN + SITE_PREFIX
EXCLUDED_PARTS = {".git", "node_modules", "__pycache__"}
MAX_GITHUB_BYTES = 100_000_000
LARGE_ASSET_BYTES = 20_000_000
LARGE_IMAGE_BYTES = 3_000_000
IMAGE_SUFFIXES = {".avif", ".gif", ".jpeg", ".jpg", ".png", ".svg", ".webp"}


@dataclass
class Issue:
    level: str
    page: str
    message: str


@dataclass
class PageData:
    path: Path
    ids: Counter[str] = field(default_factory=Counter)
    h1_count: int = 0
    main_count: int = 0
    skip_links: list[str] = field(default_factory=list)
    links: list[tuple[str, str, str]] = field(default_factory=list)
    image_alts: list[tuple[str, str | None, bool]] = field(default_factory=list)
    titles: list[str] = field(default_factory=list)
    descriptions: list[str] = field(default_factory=list)
    canonicals: list[str] = field(default_factory=list)
    metas: dict[tuple[str, str], list[str]] = field(default_factory=dict)
    json_ld: list[str] = field(default_factory=list)
    lang: str = ""
    noindex: bool = False


class PageParser(HTMLParser):
    def __init__(self, path: Path) -> None:
        super().__init__(convert_charrefs=True)
        self.data = PageData(path=path)
        self._in_title = False
        self._title_parts: list[str] = []
        self._json_script = False
        self._json_parts: list[str] = []
        self._anchor_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        values = {name.lower(): value for name, value in attrs}
        if tag == "html":
            self.data.lang = (values.get("lang") or "").strip()
        identifier = values.get("id")
        if identifier:
            self.data.ids[identifier] += 1
        if tag == "h1":
            self.data.h1_count += 1
        if tag == "main":
            self.data.main_count += 1
        if tag == "title":
            self._in_title = True
            self._title_parts = []
        if tag == "a":
            self._anchor_depth += 1
            href = (values.get("href") or "").strip()
            self.data.links.append(("a", "href", href))
            classes = (values.get("class") or "").split()
            if "skip-link" in classes:
                self.data.skip_links.append(href)
            if (values.get("target") or "").lower() == "_blank":
                rel = set((values.get("rel") or "").lower().split())
                if "noopener" not in rel:
                    self.data.links.append(("_blank", "rel", ""))
        elif tag in {"script", "img", "source", "iframe"}:
            attribute = "src"
            if values.get(attribute):
                self.data.links.append((tag, attribute, (values[attribute] or "").strip()))
        elif tag == "link":
            href = (values.get("href") or "").strip()
            rel = set((values.get("rel") or "").lower().split())
            if "canonical" in rel:
                self.data.canonicals.append(href)
            elif href:
                self.data.links.append((tag, "href", href))
        if tag == "img":
            self.data.image_alts.append(
                ((values.get("src") or "").strip(), values.get("alt"), self._anchor_depth > 0)
            )
        if tag == "meta":
            name = (values.get("name") or "").lower().strip()
            prop = (values.get("property") or "").lower().strip()
            content = (values.get("content") or "").strip()
            if name:
                self.data.metas.setdefault(("name", name), []).append(content)
            if prop:
                self.data.metas.setdefault(("property", prop), []).append(content)
            if name == "description":
                self.data.descriptions.append(content)
            if name == "robots" and "noindex" in content.lower():
                self.data.noindex = True
        if tag == "script" and (values.get("type") or "").lower() == "application/ld+json":
            self._json_script = True
            self._json_parts = []

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title" and self._in_title:
            self.data.titles.append("".join(self._title_parts).strip())
            self._in_title = False
        if tag == "script" and self._json_script:
            self.data.json_ld.append("".join(self._json_parts).strip())
            self._json_script = False
        if tag == "a" and self._anchor_depth:
            self._anchor_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self._title_parts.append(data)
        if self._json_script:
            self._json_parts.append(data)


def is_excluded(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    return any(part in EXCLUDED_PARTS or part.startswith(".tmp") for part in relative.parts)


def parse_page(path: Path) -> PageData:
    parser = PageParser(path)
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    return parser.data


def publish_candidates() -> set[Path]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return {
        (ROOT / raw.decode("utf-8")).resolve()
        for raw in result.stdout.split(b"\0")
        if raw
    }


def discover_pages() -> dict[Path, PageData]:
    discovered: dict[Path, PageData] = {}
    for path in sorted(publish_candidates()):
        if path.suffix.lower() != ".html" or not path.is_file() or is_excluded(path):
            continue
        data = parse_page(path)
        is_root_page = path.parent == ROOT
        has_public_canonical = any(value.startswith(SITE_BASE) for value in data.canonicals)
        if is_root_page or has_public_canonical:
            discovered[path.resolve()] = data
    return discovered


def expected_canonical(path: Path) -> str:
    relative = path.relative_to(ROOT).as_posix()
    if relative == "index.html":
        return SITE_BASE
    if relative.endswith("/index.html"):
        return SITE_BASE + relative[: -len("index.html")]
    return SITE_BASE + relative


def issue(issues: list[Issue], level: str, page: Path | str, message: str) -> None:
    label = page if isinstance(page, str) else page.relative_to(ROOT).as_posix()
    issues.append(Issue(level=level, page=label, message=message))


def validate_structure(data: PageData, issues: list[Issue]) -> None:
    path = data.path
    if data.lang.lower() != "en":
        issue(issues, "error", path, "html must declare lang=\"en\"")
    if data.h1_count != 1:
        issue(issues, "error", path, f"expected one h1, found {data.h1_count}")
    if data.main_count != 1:
        issue(issues, "error", path, f"expected one main, found {data.main_count}")
    if len(data.skip_links) != 1:
        issue(issues, "error", path, f"expected one skip link, found {len(data.skip_links)}")
    duplicates = sorted(identifier for identifier, count in data.ids.items() if count > 1)
    if duplicates:
        issue(issues, "error", path, f"duplicate ids: {', '.join(duplicates)}")
    for target in data.skip_links:
        if not target.startswith("#") or target[1:] not in data.ids:
            issue(issues, "error", path, f"skip link target does not exist: {target or '(empty)'}")
    for source, alt, is_linked in data.image_alts:
        if alt is None:
            issue(issues, "error", path, f"image is missing alt: {source or '(empty src)'}")
        elif not alt.strip() and is_linked:
            issue(issues, "error", path, f"linked image has empty alt: {source or '(empty src)'}")


def meta_value(data: PageData, kind: str, key: str) -> list[str]:
    return data.metas.get((kind, key), [])


def validate_metadata(data: PageData, issues: list[Issue]) -> None:
    path = data.path
    if len(data.titles) != 1 or not data.titles[0]:
        issue(issues, "error", path, "expected one non-empty title")
    if len(data.descriptions) != 1 or not data.descriptions[0]:
        issue(issues, "error", path, "expected one non-empty meta description")

    if path.name == "404.html":
        if not data.noindex:
            issue(issues, "error", path, "404 page must declare noindex")
        return

    expected = expected_canonical(path)
    if data.canonicals != [expected]:
        issue(
            issues,
            "error",
            path,
            f"canonical must be exactly {expected!r}; found {data.canonicals!r}",
        )

    required_meta = [
        ("property", "og:type"),
        ("property", "og:url"),
        ("property", "og:title"),
        ("property", "og:description"),
        ("property", "og:image"),
        ("name", "twitter:card"),
        ("name", "twitter:image"),
    ]
    for kind, key in required_meta:
        values = meta_value(data, kind, key)
        if len(values) != 1 or not values[0]:
            issue(issues, "error", path, f"expected one non-empty {key} metadata value")
    og_url = meta_value(data, "property", "og:url")
    if og_url and og_url[0] != expected:
        issue(issues, "error", path, "og:url must match canonical")
    og_image = meta_value(data, "property", "og:image")
    if og_image and not og_image[0].startswith(SITE_BASE):
        issue(issues, "error", path, "og:image must use an absolute portfolio URL")
    elif og_image:
        image_path = ROOT / unquote(urlsplit(og_image[0]).path[len(SITE_PREFIX) :])
        if not image_path.is_file():
            issue(issues, "error", path, f"og:image does not exist locally: {og_image[0]}")
    twitter_card = meta_value(data, "name", "twitter:card")
    if twitter_card and twitter_card[0] != "summary_large_image":
        issue(issues, "error", path, "twitter:card must be summary_large_image")
    twitter_image = meta_value(data, "name", "twitter:image")
    if twitter_image and og_image and twitter_image[0] != og_image[0]:
        issue(issues, "error", path, "twitter:image must match og:image")

    if not data.json_ld:
        issue(issues, "error", path, "missing JSON-LD structured data")
    for index, payload in enumerate(data.json_ld, start=1):
        try:
            parsed = json.loads(payload)
        except json.JSONDecodeError as error:
            issue(issues, "error", path, f"invalid JSON-LD block {index}: {error.msg}")
            continue
        if not isinstance(parsed, (dict, list)):
            issue(issues, "error", path, f"JSON-LD block {index} must contain an object or array")


def local_target(page: Path, raw_url: str) -> tuple[Path | None, str]:
    if not raw_url or raw_url.startswith(("mailto:", "tel:", "javascript:", "data:")):
        return None, ""
    parsed = urlsplit(raw_url)
    fragment = unquote(parsed.fragment)
    if parsed.scheme or parsed.netloc:
        if parsed.scheme not in {"http", "https"} or parsed.netloc != "singhaditya21.github.io":
            return None, fragment
        if not parsed.path.startswith(SITE_PREFIX):
            return None, fragment
        relative_url = parsed.path[len(SITE_PREFIX) :]
        target = ROOT / unquote(relative_url)
    elif parsed.path.startswith(SITE_PREFIX):
        target = ROOT / unquote(parsed.path[len(SITE_PREFIX) :])
    elif parsed.path.startswith("/"):
        return None, fragment
    elif parsed.path:
        target = page.parent / unquote(parsed.path)
    else:
        target = page

    if target.is_dir() or str(target).endswith("/"):
        target = target / "index.html"
    try:
        resolved = target.resolve()
        resolved.relative_to(ROOT.resolve())
    except ValueError:
        return Path("/__outside_site__"), fragment
    return resolved, fragment


def validate_links(pages: dict[Path, PageData], issues: list[Issue]) -> None:
    parsed_cache = dict(pages)
    for page, data in pages.items():
        for tag, attribute, raw_url in data.links:
            if tag == "_blank":
                issue(issues, "error", page, "target=_blank link is missing rel=noopener")
                continue
            target, fragment = local_target(page, raw_url)
            if target is None:
                continue
            if not target.exists():
                issue(issues, "error", page, f"broken {tag} {attribute}: {raw_url}")
                continue
            if fragment:
                if target.suffix.lower() != ".html":
                    issue(issues, "warning", page, f"fragment on non-HTML target was not checked: {raw_url}")
                    continue
                target_data = parsed_cache.get(target)
                if target_data is None:
                    target_data = parse_page(target)
                    parsed_cache[target] = target_data
                if fragment not in target_data.ids:
                    issue(issues, "error", page, f"broken fragment: {raw_url}")


def validate_social_asset(issues: list[Issue]) -> None:
    png = ROOT / "assets" / "social-preview.png"
    svg = ROOT / "assets" / "social-preview.svg"
    for path in (png, svg):
        if not path.is_file():
            issue(issues, "error", "assets", f"missing social preview: {path.relative_to(ROOT)}")
    if png.is_file():
        with png.open("rb") as handle:
            header = handle.read(24)
        if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
            issue(issues, "error", png, "social preview is not a valid PNG")
        else:
            width, height = struct.unpack(">II", header[16:24])
            if (width, height) != (1200, 630):
                issue(issues, "error", png, f"expected 1200x630, found {width}x{height}")
    if svg.is_file():
        try:
            root = ElementTree.parse(svg).getroot()
            if root.attrib.get("viewBox") != "0 0 1200 630":
                issue(issues, "error", svg, "expected viewBox 0 0 1200 630")
        except ElementTree.ParseError as error:
            issue(issues, "error", svg, f"invalid SVG XML: {error}")


def validate_discovery(pages: dict[Path, PageData], issues: list[Issue]) -> None:
    canonical_owners: dict[str, list[Path]] = {}
    for data in pages.values():
        if data.path.name == "404.html" or data.noindex or len(data.canonicals) != 1:
            continue
        canonical_owners.setdefault(data.canonicals[0], []).append(data.path)
    for canonical, owners in canonical_owners.items():
        if len(owners) > 1:
            labels = ", ".join(path.relative_to(ROOT).as_posix() for path in owners)
            issue(issues, "error", "canonicals", f"{canonical} is declared by multiple pages: {labels}")
    canonical_urls = {
        data.canonicals[0]
        for data in pages.values()
        if data.path.name != "404.html" and len(data.canonicals) == 1 and not data.noindex
    }
    sitemap = ROOT / "sitemap.xml"
    if not sitemap.is_file():
        issue(issues, "error", "sitemap.xml", "missing sitemap")
    else:
        try:
            tree = ElementTree.parse(sitemap)
            sitemap_urls = {
                element.text.strip()
                for element in tree.getroot().iter()
                if element.tag.endswith("loc") and element.text
            }
            missing = sorted(canonical_urls - sitemap_urls)
            extra = sorted(sitemap_urls - canonical_urls)
            if missing:
                issue(issues, "error", sitemap, f"missing {len(missing)} canonical URL(s)")
            if extra:
                issue(issues, "error", sitemap, f"contains {len(extra)} non-canonical URL(s)")
        except ElementTree.ParseError as error:
            issue(issues, "error", sitemap, f"invalid XML: {error}")
    robots = ROOT / "robots.txt"
    if not robots.is_file() or f"Sitemap: {SITE_BASE}sitemap.xml" not in robots.read_text(encoding="utf-8"):
        issue(issues, "error", "robots.txt", "missing absolute sitemap declaration")


def validate_file_sizes(issues: list[Issue]) -> tuple[int, int]:
    large_assets: list[tuple[int, Path]] = []
    file_count = 0
    for path in sorted(publish_candidates()):
        if not path.is_file() or is_excluded(path):
            continue
        file_count += 1
        size = path.stat().st_size
        if size >= MAX_GITHUB_BYTES:
            issue(issues, "error", path, f"{size / 1_000_000:.1f} MB exceeds GitHub's 100 MB limit")
        else:
            threshold = LARGE_IMAGE_BYTES if path.suffix.lower() in IMAGE_SUFFIXES else LARGE_ASSET_BYTES
            if size >= threshold:
                large_assets.append((size, path))
    for size, path in sorted(large_assets, reverse=True)[:12]:
        issue(issues, "warning", path, f"large public asset: {size / 1_000_000:.1f} MB")
    if len(large_assets) > 12:
        issue(issues, "warning", "files", f"{len(large_assets) - 12} additional large assets omitted")
    return file_count, len(large_assets)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--warnings-as-errors", action="store_true")
    args = parser.parse_args()

    issues: list[Issue] = []
    pages = discover_pages()
    if not pages:
        print("ERROR: no public HTML pages discovered", file=sys.stderr)
        return 1
    for data in pages.values():
        validate_structure(data, issues)
        validate_metadata(data, issues)
    validate_links(pages, issues)
    validate_social_asset(issues)
    validate_discovery(pages, issues)
    file_count, large_count = validate_file_sizes(issues)

    for item in sorted(issues, key=lambda value: (value.level != "error", value.page, value.message)):
        print(f"{item.level.upper():7} {item.page}: {item.message}")

    errors = sum(item.level == "error" for item in issues)
    warnings = sum(item.level == "warning" for item in issues)
    print(
        f"Checked {len(pages)} public HTML pages and {file_count} files: "
        f"{errors} error(s), {warnings} warning(s), {large_count} large asset(s)."
    )
    if errors or (args.warnings_as_errors and warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
