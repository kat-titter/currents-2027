#!/usr/bin/env python3
# Build [s[i/y]n[k][w]hole from src/ (its source) into synkhole/ (the built pages) of this repo, served at HOME.
# The site's root index.html only sends a visitor on to synkhole/. src/ is never published (the refill workflow leaves it out).
# It only writes files. It never commits and never pushes: publishing is Kat's, by hand.
#   python3 src/deploy.py                 every page
#   python3 src/deploy.py index.html      the piece only (about.html left as it is, e.g. while the about page is being edited)
#   python3 src/deploy.py --icon > /tmp/icon.svg && sips -s format png -z 180 180 /tmp/icon.svg --out synkhole/apple-touch-icon.png
#                                         redraws the home-screen icon after the icon changes (sips is macOS's)
# Writes synkhole/index.html (the piece), synkhole/about.html (the page about the piece, with index.html's thirst model put in at its // <thirst> line), and at the root index.html (sends a visitor
# on to synkhole/) and .nojekyll. README.md is written by hand; this only checks that it still names HOME.
# Binaries live once, in the built folder, never in src/: the about page's pictures in synkhole/doc/ (here only checked: every picture
# about.html names is there), the reservoir in synkhole/reservoir/ (stored dreams for when the spring sleeps, made by src/reservoir.py
# or by the refill; here only checked: whole, and 6 MB at most; no reservoir, nothing written: without it the basin is dry), and a link
# preview picture, synkhole/og.jpg (1200 x 630, the piece itself with its title), whose tags are added when it is there. The tab icon is
# no file: icon() below draws its SVG, inline in each page's <head>; synkhole/apple-touch-icon.png is that SVG at 180 px, full bleed.
# Vanitas Veritas is a separate piece with its own script (verse/deploy_verse.py) and its own address; nothing here writes to it.
import json, math, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent                # src/: the source
DEST = HERE.parent                                             # the repo, which is the site (Kat, 2026-11-17: "Yes, currents-2027")
SITE = DEST / 'synkhole'                                       # the piece inside it
HOME = 'https://kat-titter.github.io/currents-2027/synkhole/'  # the piece's public address: change it here and in the veritas forwarding pages

FILM = ('#59e6ff', '#9e7aff', '#ff73b8')      # the water's film, cyan to violet to rose (kiri() in index.html); no gold
PEARL = ('#bfe6ee', '#cfc9f2', '#f2c9dd')     # the hole's thin ring (--pearl in index.html)
def film(t):                                  # a colour along the film, t from 0 (cyan) to 1 (rose)
    a, b, u = (FILM[0], FILM[1], 2*t) if t < .5 else (FILM[1], FILM[2], 2*t - 1)
    return '#' + ''.join(f'{round(int(a[k:k+2], 16)*(1 - u) + int(b[k:k+2], 16)*u):02x}' for k in (1, 3, 5))
def icon(bleed=False):                        # the tab icon, the fall: the piece's dot grid swirling into the hole, in a squircle, on ink
    dots = []
    for i in range(8):
        for j in range(8):                    # an 8 x 8 grid, pulled in toward the hole and turned a little as it falls
            x, y = 4 + 8*j, 4 + 8*i; dx, dy = x - 32, y - 32; r = math.hypot(dx, dy); rr = r - 64/r
            if rr < 11: continue
            a = math.atan2(dy, dx) + 16/r; px, py = rr*math.cos(a), rr*math.sin(a); rad = 1.5 + 1.8*min(1, (rr - 11)/16)   # smaller as they fall in
            if (abs(px)**3.2 + abs(py)**3.2)**(1/3.2) > 29.5 - rad: continue   # the field's edge: a squircle, between square and circle (Kat)
            dots.append(f"<circle cx='{32 + px:.1f}' cy='{32 + py:.1f}' r='{rad:.1f}' fill='{film(min(1, max(0, (x + y - 8)/112)))}'/>")
    ring = "<linearGradient id='p' x1='0' y1='0' x2='1' y2='1'>" + ''.join(f"<stop offset='{o}' stop-color='{c}'/>" for o, c in zip(('0', '.5', '1'), PEARL))
    corner = '' if bleed else " rx='14'"      # full bleed for the home screen, whose corners iOS rounds itself
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'><defs>{ring}</linearGradient></defs><rect width='64' height='64'{corner} fill='#030304'/>"
            f"{''.join(dots)}<circle cx='32' cy='32' r='9.5' fill='url(#p)'/><circle cx='32' cy='32' r='7.5' fill='#000'/></svg>")
ICON = ('<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,' + icon().replace('#', '%23').replace('<', '%3C').replace('>', '%3E') + '">\n'
        f'<link rel="apple-touch-icon" href="{HOME}apple-touch-icon.png">\n')   # that SVG at 180 px, drawn by the --icon recipe at the top

def reservoir():                                          # the stored dreams: checked, never built here
    res = SITE / 'reservoir'
    if not (res / 'index.json').exists(): sys.exit(f'no reservoir in {SITE}: fill it with synkhole/reservoir.py first; nothing written')
    runs = json.loads((res / 'index.json').read_text())['runs']; total = sum(f.stat().st_size for f in res.iterdir())
    missing = [f for r in runs for f in r if not (res / f).exists()]
    if missing or total > 6_000_000: sys.exit(f'reservoir: {len(missing)} listed frames missing, {total} bytes (6,000,000 at most); nothing written')
    return f'reservoir: {len(runs)} dreams, {sum(len(r) for r in runs)} frames, {total} bytes'

def preview(html, name):                                  # what a shared link unfurls with, and the tab's icon
    title = re.search(r'<title>(.*?)</title>', html).group(1); desc = re.search(r'<meta name="description" content="([^"]*)">', html)
    tags = (f'<meta property="og:title" content="{title}">\n' + (f'<meta property="og:description" content="{desc.group(1)}">\n' if desc else '')
            + f'<meta property="og:type" content="website">\n<meta property="og:url" content="{HOME}{"" if name == "index.html" else name}">\n')
    if (SITE / 'og.jpg').exists():
        tags += (f'<meta property="og:image" content="{HOME}og.jpg">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
                 f'<meta name="twitter:image" content="{HOME}og.jpg">\n<meta name="twitter:card" content="summary_large_image">\n')
    tags += ICON
    if '<meta charset="utf-8">\n' not in html: sys.exit(f'{name}: no <meta charset="utf-8"> line to put the preview tags after; nothing written')
    return html.replace('<meta charset="utf-8">\n', '<meta charset="utf-8">\n' + tags, 1)

FORWARD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CURRENTS 2027, Kat Titterton</title>
<meta http-equiv="refresh" content="0; url=synkhole/">
<style>body{margin:0;background:#030304} a{color:#8a8d93;font:12px ui-monospace,Menlo,monospace;padding:20px;display:block}</style>
</head>
<body><a href="synkhole/">[s[i/y]n[k][w]hole</a></body>
</html>
"""

if '--icon' in sys.argv: print(icon(bleed=True)); sys.exit()
NAMES = [a for a in sys.argv[1:] if a in ('index.html', 'about.html')] or ['index.html', 'about.html']
if 'about.html' in NAMES and not (HERE / 'about.html').exists(): sys.exit('src/about.html is missing and the piece links to it; nothing written')
SITE.mkdir(parents=True, exist_ok=True)
print(reservoir())
pages = {name: (HERE / name).read_text() for name in NAMES}
THIRST = re.search(r'^// <thirst>.*?^// </thirst>[^\n]*$', (HERE / 'index.html').read_text(), re.S | re.M)   # the thirst model's one home: index.html, between these two lines
if not THIRST: sys.exit('src/index.html has no // <thirst> ... // </thirst> block (the thirst model); nothing written')
if 'about.html' in pages:                                     # the about page's days figure draws from that same code: it goes in at the page's own // <thirst> line
    marks = re.findall(r'^// <thirst>[^\n]*$', pages['about.html'], re.M)
    if len(marks) != 1 or '// </thirst>' in pages['about.html']: sys.exit('src/about.html needs one // <thirst> line, where the thirst model goes, and no copy of its own; nothing written')
    pages['about.html'] = pages['about.html'].replace(marks[0], THIRST.group(0), 1)
stale = [w for w in ['sync.html?', 'dry_season.html', 'github.io/veritas/about'] if w in pages.get('about.html', '')]     # addresses the piece had under veritas on 2026-11-17
if stale: sys.exit(f'about.html still points at {", ".join(stale)}: the old addresses; nothing written')
lost = sorted({p for p in re.findall(r'\bdoc/[\w.-]+\.webp', pages.get('about.html', '')) if not (SITE / p).exists()})   # pictures live in synkhole/doc/ only
if lost: sys.exit(f'about.html names {len(lost)} pictures missing from {SITE / "doc"}: {", ".join(lost)}; nothing written')
for name, html in pages.items(): (SITE / name).write_text(preview(html, name))
(DEST / 'index.html').write_text(preview(FORWARD, 'index.html'))   # the root unfurls as the piece
(DEST / '.nojekyll').write_text('')
if HOME not in (DEST / 'README.md').read_text(): print('README.md does not name', HOME, '- update its links by hand')
print('wrote', ', '.join('synkhole/' + n for n in pages) + ', and index.html at the root of', DEST)
print('not committed, not pushed: that is done by hand in', DEST)
