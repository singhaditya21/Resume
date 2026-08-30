#!/usr/bin/env python3
"""Generate the portfolio sitemap from canonical HTML metadata.

Only pages that explicitly declare a canonical URL inside SITE_BASE are
published. This keeps private working HTML and local reference material out of
the sitemap while automatically discovering new public collection pages.
"""

from __future__ import annotations

import argparse
import subprocess
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
SITE_BASE = "https://singhaditya21.github.io/Resume/"
OUTPUT = ROOT / "sitemap.xml"
EXCLUDED_PARTS = {".git", "node_modules", "__pycache__"}


class CanonicalParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.canonicals: list[str] = []
        self.noindex = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {name.lower(): value or "" for name, value in attrs}
        if tag.lower() == "link" and "canonical" in values.get("rel", "").lower().split():
            if values.get("href"):
                self.canonicals.append(values["href"].strip())
        if tag.lower() == "meta" and values.get("name", "").lower() == "robots":
            self.noindex = "noindex" in values.get("content", "").lower()


def public_html_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    pages: list[Path] = []
    for raw in result.stdout.split(b"\0"):
        if not raw:
            continue
        path = ROOT / raw.decode("utf-8")
        if path.suffix.lower() != ".html" or not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        if any(part in EXCLUDED_PARTS or part.startswith(".tmp") for part in relative.parts):
            continue
        pages.append(path)
    return sorted(pages)


def normalized_canonical(value: str) -> str | None:
    parsed = urlsplit(value)
    if parsed.scheme != "https" or parsed.netloc != "singhaditya21.github.io":
        return None
    if not parsed.path.startswith("/Resume/") or parsed.query or parsed.fragment:
        return None
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", ""))


def discover_urls() -> list[str]:
    urls: set[str] = set()
    for page in public_html_files():
        parser = CanonicalParser()
        parser.feed(page.read_text(encoding="utf-8"))
        parser.close()
        if parser.noindex:
            continue
        if len(parser.canonicals) > 1:
            raise ValueError(f"Multiple canonical links in {page.relative_to(ROOT)}")
        if not parser.canonicals:
            continue
        canonical = normalized_canonical(parser.canonicals[0])
        if canonical is None:
            raise ValueError(
                f"Canonical is outside {SITE_BASE} or contains a query/fragment: "
                f"{page.relative_to(ROOT)}"
            )
        urls.add(canonical)
    return sorted(urls, key=lambda url: (url != SITE_BASE, url))


def render_sitemap(urls: list[str]) -> str:
    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ElementTree.register_namespace("", namespace)
    root = ElementTree.Element(f"{{{namespace}}}urlset")
    for url in urls:
        entry = ElementTree.SubElement(root, f"{{{namespace}}}url")
        ElementTree.SubElement(entry, f"{{{namespace}}}loc").text = url
    ElementTree.indent(root, space="  ")
    # ElementTree's XML declaration casing differs between supported Python
    # versions. Emit it ourselves so --check is deterministic locally and in CI.
    body = ElementTree.tostring(root, encoding="unicode", xml_declaration=False)
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + body + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail when sitemap.xml is not identical to the generated result.",
    )
    args = parser.parse_args()

    urls = discover_urls()
    if not urls:
        raise SystemExit("No canonical public pages discovered.")
    rendered = render_sitemap(urls)

    if args.check:
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        if current != rendered:
            print("sitemap.xml is stale; run: python3 scripts/generate_sitemap.py")
            return 1
        print(f"sitemap.xml is current ({len(urls)} canonical pages).")
        return 0

    OUTPUT.write_text(rendered, encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} with {len(urls)} canonical pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
