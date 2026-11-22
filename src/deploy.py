#!/usr/bin/env python3
# Build [s[i/y]n[k][w]hole from src/ (its source) into synkhole/ (the built pages) of this repo, served at HOME.
# The site's root index.html only sends a visitor on to synkhole/. src/ is never published (the refill workflow leaves it out).
# It only writes files. It never commits and never pushes: publishing is Kat's, by hand.
#   python3 src/deploy.py                 every page
#   python3 src/deploy.py index.html      the piece only (about.html left as it is, e.g. while the about page is being edited)
# Writes synkhole/index.html (the piece), synkhole/about.html (the page about the piece), and at the root index.html (sends a visitor
# on to synkhole/), README.md and .nojekyll.
# Binaries live once, in the built folder, never in src/: the about page's pictures in synkhole/doc/ (here only checked: every picture
# about.html names is there), the reservoir in synkhole/reservoir/ (stored dreams for when the spring sleeps, made by src/reservoir.py
# or by the refill; here only checked: whole, and 6 MB at most; no reservoir, nothing written: without it the basin is dry), and a link
# preview picture, synkhole/og.jpg (1200 x 630, the piece itself with its title), whose tags are added when it is there. The tab icon is
# no file: its SVG sits inline in each page's <head>; synkhole/apple-touch-icon.png is that SVG drawn at 180 px, full bleed.
# Vanitas Veritas is a separate piece with its own script (verse/deploy_verse.py) and its own address; nothing here writes to it.
import json, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent                # src/: the source
DEST = HERE.parent                                             # the repo, which is the site (Kat, 2026-11-17: "Yes, currents-2027")
SITE = DEST / 'synkhole'                                       # the piece inside it
HOME = 'https://kat-titter.github.io/currents-2027/synkhole/'  # the piece's public address: change it here and in the veritas forwarding pages

def reservoir():                                          # the stored dreams: checked, never built here
    res = SITE / 'reservoir'
    if not (res / 'index.json').exists(): sys.exit(f'no reservoir in {SITE}: fill it with synkhole/reservoir.py first; nothing written')
    runs = json.loads((res / 'index.json').read_text())['runs']; total = sum(f.stat().st_size for f in res.iterdir())
    missing = [f for r in runs for f in r if not (res / f).exists()]
    if missing or total > 6_000_000: sys.exit(f'reservoir: {len(missing)} listed frames missing, {total} bytes (6,000,000 at most); nothing written')
    return f'reservoir: {len(runs)} dreams, {sum(len(r) for r in runs)} frames, {total} bytes'

def preview(html, name):                                  # what a shared link unfurls with
    title = re.search(r'<title>(.*?)</title>', html).group(1); desc = re.search(r'<meta name="description" content="([^"]*)">', html)
    tags = (f'<meta property="og:title" content="{title}">\n' + (f'<meta property="og:description" content="{desc.group(1)}">\n' if desc else '')
            + f'<meta property="og:type" content="website">\n<meta property="og:url" content="{HOME}{"" if name == "index.html" else name}">\n')
    if (SITE / 'og.jpg').exists():
        tags += (f'<meta property="og:image" content="{HOME}og.jpg">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
                 f'<meta name="twitter:image" content="{HOME}og.jpg">\n<meta name="twitter:card" content="summary_large_image">\n')
    if '<meta charset="utf-8">\n' not in html: sys.exit(f'{name}: no <meta charset="utf-8"> line to put the preview tags after; nothing written')
    return html.replace('<meta charset="utf-8">\n', '<meta charset="utf-8">\n' + tags, 1)

FORWARD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CURRENTS 2027, Kat Titterton</title>
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Cdefs%3E%3ClinearGradient id='p' x1='0' y1='0' x2='1' y2='1'%3E%3Cstop offset='0' stop-color='%23bfe6ee'/%3E%3Cstop offset='.5' stop-color='%23cfc9f2'/%3E%3Cstop offset='1' stop-color='%23f2c9dd'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='64' height='64' rx='14' fill='%23030304'/%3E%3Ccircle cx='32.0' cy='8.0' r='4' fill='%237cb0ff'/%3E%3Ccircle cx='44.0' cy='11.2' r='4' fill='%2364d4ff'/%3E%3Ccircle cx='52.8' cy='20.0' r='4' fill='%2364d4ff'/%3E%3Ccircle cx='56.0' cy='32.0' r='4' fill='%237cb0ff'/%3E%3Ccircle cx='52.8' cy='44.0' r='4' fill='%23928cff'/%3E%3Ccircle cx='44.0' cy='52.8' r='4' fill='%23ae79f3'/%3E%3Ccircle cx='32.0' cy='56.0' r='4' fill='%23ce76dc'/%3E%3Ccircle cx='20.0' cy='52.8' r='4' fill='%23ef74c4'/%3E%3Ccircle cx='11.2' cy='44.0' r='4' fill='%23ef74c4'/%3E%3Ccircle cx='8.0' cy='32.0' r='4' fill='%23ce76dc'/%3E%3Ccircle cx='11.2' cy='20.0' r='4' fill='%23ae79f3'/%3E%3Ccircle cx='20.0' cy='11.2' r='4' fill='%23938cff'/%3E%3Ccircle cx='32' cy='32' r='14.1' fill='url(%23p)'/%3E%3Ccircle cx='32' cy='32' r='11.9' fill='%23000'/%3E%3C/svg%3E">
<link rel="apple-touch-icon" href="synkhole/apple-touch-icon.png">
<meta http-equiv="refresh" content="0; url=synkhole/">
<style>body{margin:0;background:#030304} a{color:#8a8d93;font:12px ui-monospace,Menlo,monospace;padding:20px;display:block}</style>
</head>
<body><a href="synkhole/">[s[i/y]n[k][w]hole</a></body>
</html>
"""
README = f"""# currents-2027

Kat Titterton's work for CURRENTS 2027, Santa Fe.

- [s[i/y]n[k][w]hole: {HOME}
- about the piece: {HOME}about.html

By Kat Titterton (macrofluidic). An evolution of Vanitas Veritas, an earlier sink, which keeps its own address: https://kat-titter.github.io/veritas/

- `src/`: the source of the piece and its about page; `python3 src/deploy.py` builds them into `synkhole/`. Never published.
- `synkhole/`: the built pages, with `doc/` (the about page's pictures) and `reservoir/` (stored dreams, from `src/reservoir.py` or the refill).
- `refill/`: dreams new water on a runner (`.github/workflows/refill.yml`).
- `src/archive/`: three versions of the piece from 17 Nov and the script that built them, retired.
"""

NAMES = [a for a in sys.argv[1:] if a in ('index.html', 'about.html')] or ['index.html', 'about.html']
if 'about.html' in NAMES and not (HERE / 'about.html').exists(): sys.exit('src/about.html is missing and the piece links to it; nothing written')
SITE.mkdir(parents=True, exist_ok=True)
print(reservoir())
pages = {name: (HERE / name).read_text() for name in NAMES}
stale = [w for w in ['sync.html?', 'dry_season.html', 'github.io/veritas/about'] if w in pages.get('about.html', '')]     # addresses the piece had under veritas on 2026-11-17
if stale: sys.exit(f'about.html still points at {", ".join(stale)}: the old addresses; nothing written')
lost = sorted({p for p in re.findall(r'\bdoc/[\w.-]+\.webp', pages.get('about.html', '')) if not (SITE / p).exists()})   # pictures live in synkhole/doc/ only
if lost: sys.exit(f'about.html names {len(lost)} pictures missing from {SITE / "doc"}: {", ".join(lost)}; nothing written')
for name, html in pages.items(): (SITE / name).write_text(preview(html, name))
(DEST / 'index.html').write_text(FORWARD)
(DEST / '.nojekyll').write_text('')
(DEST / 'README.md').write_text(README)
print('wrote', ', '.join('synkhole/' + n for n in pages) + ', and index.html, README.md at the root of', DEST)
print('not committed, not pushed: that is done by hand in', DEST)
