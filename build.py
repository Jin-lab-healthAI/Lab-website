#!/usr/bin/env python3
"""Static site generator for the Jin Lab website.

Reads YAML from content/, renders Jinja2 templates from templates/,
copies static/ verbatim, and writes everything to _site/.

    python build.py            # build once into _site/
    python build.py --serve    # build, then serve on http://localhost:8000

Everything a non-developer needs to change lives in content/*.yml.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import re
import shutil
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from markupsafe import Markup

ROOT = Path(__file__).parent.resolve()
CONTENT = ROOT / "content"
TEMPLATES = ROOT / "templates"
STATIC = ROOT / "static"
OUT = ROOT / "_site"

PAGES = {
    "index.html": "index.html",
    "research.html": "research.html",
    "publications.html": "publications.html",
    "people.html": "people.html",
    "join.html": "join.html",
}


def load_content() -> dict:
    data = {}
    for path in sorted(CONTENT.glob("*.yml")):
        with path.open(encoding="utf-8") as fh:
            data[path.stem] = yaml.safe_load(fh) or {}
    missing = {"site", "research", "people", "publications", "news", "join"} - data.keys()
    if missing:
        sys.exit(f"missing content files: {', '.join(sorted(missing))}")
    return data


def make_env(site: dict) -> Environment:
    env = Environment(
        loader=FileSystemLoader(TEMPLATES),
        autoescape=True,
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    base = (site.get("base_url") or "").rstrip("/")

    def asset(path: str) -> str:
        """Prefix a site-relative path with base_url (for project pages)."""
        return f"{base}/{str(path).lstrip('/')}" if base else str(path).lstrip("/")

    def highlight(authors: str, names: list[str]) -> Markup:
        """Bold the lab's own author names inside an author string."""
        out = html.escape(authors)
        for name in sorted(names, key=len, reverse=True):
            safe = html.escape(name)
            out = re.sub(rf"(?<![\w>]){re.escape(safe)}(?![\w])", f"<strong>{safe}</strong>", out)
        return Markup(out)

    def initials(name: str) -> str:
        parts = [p for p in re.split(r"[\s,]+", name) if p and p[0].isalpha()]
        return "".join(p[0] for p in parts[:2]).upper()

    def slug(text: str) -> str:
        return re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")

    env.filters.update(asset=asset, highlight=highlight, initials=initials, slug=slug)
    env.globals.update(
        asset=asset,
        now=dt.datetime.now(dt.timezone.utc),
        year=dt.datetime.now(dt.timezone.utc).year,
    )
    return env


def group_publications(pubs: list[dict]) -> list[tuple[int, list[dict]]]:
    years = sorted({p["year"] for p in pubs}, reverse=True)
    return [(y, [p for p in pubs if p["year"] == y]) for y in years]


def write_sitemap(site: dict, pages: list[str]) -> None:
    root = (site.get("site_url") or "").rstrip("/") + (site.get("base_url") or "").rstrip("/")
    today = dt.date.today().isoformat()
    urls = "\n".join(
        f"  <url><loc>{root}/{p}</loc><lastmod>{today}</lastmod></url>" for p in pages
    )
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n</urlset>\n",
        encoding="utf-8",
    )
    (OUT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {root}/sitemap.xml\n", encoding="utf-8"
    )


def build() -> None:
    data = load_content()
    site = data["site"]
    env = make_env(site)

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    shutil.copytree(STATIC, OUT / "static")
    (OUT / ".nojekyll").touch()
    for extra in ("CNAME",):
        if (ROOT / extra).exists():
            shutil.copy2(ROOT / extra, OUT / extra)

    pubs = data["publications"]["publications"]
    ctx = {
        "site": site,
        "research": data["research"],
        "people": data["people"],
        "pubs": data["publications"],
        "publications": pubs,
        "pub_years": group_publications(pubs),
        "pub_types": sorted({p.get("type", "journal") for p in pubs}),
        "selected_pubs": [p for p in pubs if p.get("selected")],
        "news": data["news"]["items"],
        "join": data["join"],
    }

    for out_name, template_name in PAGES.items():
        page = env.get_template(template_name).render(page_name=out_name, **ctx)
        (OUT / out_name).write_text(page, encoding="utf-8")
        print(f"  wrote _site/{out_name}  ({len(page):,} bytes)")

    write_sitemap(site, list(PAGES))
    print(f"built {len(PAGES)} pages into {OUT.relative_to(ROOT)}/")


def serve(port: int = 8000) -> None:
    import functools
    import http.server
    import socketserver

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(OUT))
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"serving http://localhost:{port}  (Ctrl-C to stop)")
        httpd.serve_forever()


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--serve", action="store_true", help="serve _site/ after building")
    ap.add_argument("--port", type=int, default=8000)
    args = ap.parse_args()
    build()
    if args.serve:
        serve(args.port)
