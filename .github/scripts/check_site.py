#!/usr/bin/env python3
"""Check the static site before it is published.

Every page must carry the same safety and accessibility basics, every
internal link must point at a file that exists, and nothing may be
loaded from another origin: the pages declare a Content Security Policy
that allows only same-origin styles and images, so a stray external
resource or inline style would silently break in the browser.

Usage: check_site.py <site directory>
"""

from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

REQUIRED_CSP = (
    "default-src 'none'; style-src 'self'; img-src 'self'; "
    "base-uri 'none'; form-action 'none'"
)
PAGE_BASE = "/sunucu-yedek/"


class Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.doctype = False
        self.lang = None
        self.title = False
        self.metas: dict[str, str] = {}
        self.charset = False
        self.links: list[tuple[str, str]] = []
        self.problems: list[str] = []
        self._in_title = False

    def handle_decl(self, decl: str) -> None:
        if decl.lower() == "doctype html":
            self.doctype = True

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k: (v or "") for k, v in attrs}
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            if "charset" in a:
                self.charset = a["charset"].lower() == "utf-8"
            key = a.get("name") or a.get("http-equiv")
            if key:
                self.metas[key.lower()] = a.get("content", "")
        elif tag in ("script", "style", "iframe", "form", "object", "embed"):
            self.problems.append(f"<{tag}> is not allowed")
        if "style" in a:
            self.problems.append(f"inline style attribute on <{tag}>")
        for attr in ("href", "src"):
            if attr in a:
                self.links.append((tag, a[attr]))

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title and data.strip():
            self.title = True


def check(site: Path) -> list[str]:
    errors: list[str] = []
    pages = sorted(site.rglob("*.html"))
    if not pages:
        return [f"no pages found in {site}"]
    for page in pages:
        rel = page.relative_to(site).as_posix()
        p = Page()
        p.feed(page.read_text(encoding="utf-8"))
        found = list(p.problems)
        if not p.doctype:
            found.append("missing <!doctype html>")
        if not p.lang:
            found.append("missing <html lang>")
        if not p.charset:
            found.append("missing <meta charset=utf-8>")
        if not p.title:
            found.append("missing <title>")
        for name in ("viewport", "description", "referrer"):
            if not p.metas.get(name):
                found.append(f"missing <meta name={name}>")
        if p.metas.get("content-security-policy") != REQUIRED_CSP:
            found.append("Content-Security-Policy differs from the site policy")
        for tag, url in p.links:
            parts = urlsplit(url)
            if parts.scheme in ("http", "https"):
                if parts.scheme != "https":
                    found.append(f"insecure link: {url}")
                if tag != "a":
                    found.append(f"external resource on <{tag}>: {url}")
                continue
            if parts.scheme or url.startswith("//"):
                found.append(f"unexpected link: {url}")
                continue
            path = parts.path
            if not path:
                continue
            if path.startswith("/"):
                if not path.startswith(PAGE_BASE):
                    found.append(f"absolute link outside the site: {url}")
                    continue
                target = site / path[len(PAGE_BASE):]
            else:
                target = page.parent / path
            if path.endswith("/"):
                target = target / "index.html"
            if not target.resolve().is_file():
                found.append(f"broken link: {url}")
        errors.extend(f"{rel}: {f}" for f in found)
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__.strip().splitlines()[-1], file=sys.stderr)
        return 2
    site = Path(sys.argv[1])
    errors = check(site)
    for e in errors:
        print(e)
    count = len(list(site.rglob("*.html")))
    print(f"{count} pages checked, {len(errors)} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
