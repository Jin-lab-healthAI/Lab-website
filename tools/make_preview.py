#!/usr/bin/env python3
"""Bundle the built home page into one self-contained HTML file.

CSS, JS, and every image are inlined, so the result opens correctly from a
file path, an email attachment, or a chat message — no server, no assets
folder. Useful for circulating a design draft before the site is public.

    python build.py && python tools/make_preview.py
    # -> jin-lab-preview.html
"""

from __future__ import annotations

import base64
import mimetypes
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
OUT = ROOT / "jin-lab-preview.html"

# In a one-file preview the other pages don't exist; point their links at the
# matching home-page sections instead of dead files.
LINK_MAP = {
    "research.html": "#research",
    "publications.html": "#publications",
    "people.html": "#people",
    "join.html": "#collaborators",
    "index.html": "#main",
}


def main() -> None:
    page = SITE / "index.html"
    if not page.exists():
        sys.exit("run `python build.py` first")

    html = page.read_text(encoding="utf-8")
    css = (SITE / "static/css/style.css").read_text(encoding="utf-8")
    js = (SITE / "static/js/main.js").read_text(encoding="utf-8")

    html = re.sub(r'<link rel="stylesheet" href="[^"]*style\.css">', f"<style>\n{css}\n</style>", html)
    html = re.sub(r'<script src="[^"]*main\.js"></script>', f"<script>\n{js}\n</script>", html)

    for ref in sorted(set(re.findall(r'"((?:[^"]*/)?static/img/[^"]+)"', html))):
        path = SITE / ref.lstrip("/")
        if not path.exists():
            continue
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        data = base64.b64encode(path.read_bytes()).decode()
        html = html.replace(f'"{ref}"', f'"data:{mime};base64,{data}"')

    for target, anchor in LINK_MAP.items():
        html = html.replace(f'href="{target}"', f'href="{anchor}"')

    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT.name}  ({OUT.stat().st_size / 1e6:.1f} MB, fully self-contained)")


if __name__ == "__main__":
    main()
