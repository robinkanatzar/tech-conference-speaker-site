#!/usr/bin/env python3
"""Shared header and footer for techconferencespeaker.com.

Change the tabs or footer here, then run:

    python3 tools/site.py

It rewrites the <header> and <footer> of every page in the repo, and marks the right tab as the
current page. The content of each page is never touched.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://techconferencespeaker.com"
NAME = "Tech Conference Speaker"
EMAIL = "hello@robinkanatzar.com"

TABS = [  # (label, href, key); the key is the page's folder name
    ("Get a mentor", "/speakers/", "speakers"),
    ("Be a mentor", "/mentors/", "mentors"),
    ("For conferences", "/conferences/", "conferences"),
    ("About", "/about/", "about"),
]

FOOTER = f"""<footer class="site-footer">
  <div class="wrap">
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/about/">About</a></li>
      <li><a href="/accessibility/">Accessibility</a></li>
      <li><a href="mailto:{EMAIL}">Contact<span class="sr-only"> (opens your email app)</span></a></li>
    </ul>
    <p>© 2026 Robin Kanatzar. This site uses no cookies and no trackers. Typeface: Atkinson Hyperlegible Next, by the Braille Institute.</p>
  </div>
</footer>"""


def header(active: str | None) -> str:
    items = "\n".join(
        f'        <li><a href="{href}"{" aria-current=" + chr(34) + "page" + chr(34) if key == active else ""}>{label}</a></li>'
        for label, href, key in TABS
    )
    return f"""<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/">{NAME}</a>
    <nav class="site-nav" aria-label="Main">
      <ul>
{items}
      </ul>
    </nav>
  </div>
</header>"""


def head(title: str, description: str, path: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:title" content="{title}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:description" content="{description}">
<link rel="preload" href="/fonts/atkinson-hyperlegible-next-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/styles.css">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def tab_for(path: str) -> str | None:
    first = path.strip("/").split("/")[0]
    return first if any(first == key for _, _, key in TABS) else None


def page(*, path: str, title: str, description: str, body: str, script: str = "") -> str:
    """A full page: head, shared header (tab chosen from the path), body, footer. Used to make new pages."""
    return (head(title, description, path) + header(tab_for(path))
            + f'\n\n<main id="main">\n{body.strip()}\n</main>\n\n{FOOTER}\n{script}</body>\n</html>\n')


def apply_chrome() -> list[Path]:
    """Rewrite the header and footer of every page from TABS and FOOTER."""
    changed = []
    for f in sorted(ROOT.rglob("*.html")):
        if ".git" in f.parts:
            continue
        rel = "/" + f.relative_to(ROOT).as_posix()
        url = rel[: -len("index.html")] if rel.endswith("index.html") else rel
        s = f.read_text()
        new = re.sub(r'<header class="site-header">.*?</header>', lambda _: header(tab_for(url)), s, flags=re.S)
        new = re.sub(r'<footer class="site-footer">.*?</footer>', lambda _: FOOTER, new, flags=re.S)
        if new != s:
            f.write_text(new)
            changed.append(f)
    return changed


if __name__ == "__main__":
    for f in apply_chrome():
        print("updated", f.relative_to(ROOT))
