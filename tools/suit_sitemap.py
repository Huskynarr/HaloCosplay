#!/usr/bin/env python3
"""Generate sitemap.xml from the published pages and Markdown guides."""
import argparse
from pathlib import Path
import sys
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://huskynarr.github.io/HaloCosplay/"
PAGES = ("", "web/", "web/configurator/", "web/budget/", "web/products/", "web/cortana/")
# Not published or not meant for readers (see the copy step in .github/workflows/pages.yml).
EXCLUDED_DIRS = {".git", ".github", "build", "docs", "node_modules", "tools"}
EXCLUDED_FILES = {"CLAUDE.md"}


def guides(root=ROOT):
    result = []
    for path in root.rglob("*.md"):
        relative = path.relative_to(root)
        if relative.parts[0] in EXCLUDED_DIRS or relative.as_posix() in EXCLUDED_FILES:
            continue
        if relative.parts[:2] in (("Tests", "Automation"), ("Tests", "Browser"), ("web", "vendor")):
            continue
        result.append(relative.as_posix())
    return sorted(result)


def render(root=ROOT):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for page in PAGES:
        if not (root / page / "index.html").is_file():
            raise ValueError("Missing page: " + (page or "index.html"))
        lines.append(f"  <url><loc>{escape(BASE + page)}</loc><priority>1.0</priority></url>")
    lines += [f"  <url><loc>{escape(BASE + name)}</loc><priority>0.7</priority></url>" for name in guides(root)]
    return "\n".join(lines + ["</urlset>", ""])


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if sitemap.xml is out of date")
    args = parser.parse_args(argv)
    target = ROOT / "sitemap.xml"
    try:
        content = render()
        if args.check:
            if not target.is_file() or target.read_text(encoding="utf-8") != content:
                raise ValueError("sitemap.xml missing/out of date; run python3 tools/suit_sitemap.py")
        else:
            target.write_text(content, encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"Sitemap error: {exc}", file=sys.stderr)
        return 2
    print(f"{len(PAGES)} pages, {len(guides())} guides")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
