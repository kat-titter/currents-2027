#!/usr/bin/env python3
# Fill the reservoir: the stored dreams [syn[k]]hole pours when no spring answers (src/index.html, `reservoir` in its LOOK).
# The frames come from a folder banked while the spring ran: its small frames (f<seq>_s.jpg), and frames.jsonl with one
# line for each frame logged while banking (seq, prompt, whether a face was at the sink). The longest unbroken run of
# frame numbers is the walk. A frame logged with a face at the sink, or with --oref in its prompt, is never taken: the walk
# is cut there. The walk is then cut into equal passages (the page pours them in a fresh order each visit, and the frames
# of a passage in order), each of --frames frames, one in every few so the passages span the whole walk.
# The reservoir lives only in the built folder, synkhole/reservoir/ (as og.jpg does), 6 MB in all at most: src/ gains no binary.
#   python3 src/reservoir.py <banked folder> [--passages 6] [--frames 10] [--width 1024] [--every 5]
# writes synkhole/reservoir/ of this repo: index.json and a00.jpg, a01.jpg ... (a, b, c: the passages; 00, 01: their frames in order)
import argparse, datetime, json, pathlib, re, shutil, sys
from PIL import Image
ap = argparse.ArgumentParser(); ap.add_argument('src'); ap.add_argument('--passages', type=int, default=6); ap.add_argument('--frames', type=int, default=10)
ap.add_argument('--width', type=int, default=1024); ap.add_argument('--every', type=float, default=5); ap.add_argument('--budget', type=int, default=5_900_000)
a = ap.parse_args(); SRC = pathlib.Path(a.src); DEST = pathlib.Path(__file__).resolve().parent.parent / 'synkhole/reservoir'
log = {r['seq']: r for r in (json.loads(l) for l in (SRC / 'frames.jsonl').read_text().splitlines() if l.strip())}
faced = lambda s: bool(log.get(s, {}).get('face')) or '--oref' in (log.get(s, {}).get('prompt') or '')
seqs = sorted(int(m.group(1)) for m in (re.match(r'f(\d+)_s\.jpg$', f.name) for f in SRC.iterdir()) if m)
walks = []                                              # unbroken runs of frame numbers, cut at any frame dreamed with a face
for s in seqs:
    if faced(s): walks.append([]); continue
    if walks and walks[-1] and walks[-1][-1] == s - 1: walks[-1].append(s)
    else: walks.append([s])
walk = max(walks, key=len); need = a.passages*a.frames; step = len(walk)//need
if step < 1: sys.exit(f'the longest walk has {len(walk)} frames; {need} are needed')
walk = walk[(len(walk) - need*step)//2:][:need*step]
picks = [[walk[(p*a.frames + i)*step] for i in range(a.frames)] for p in range(a.passages)]
def pack(width, q):
    if DEST.exists(): shutil.rmtree(DEST)
    DEST.mkdir(parents=True); runs = []
    for p, frames in enumerate(picks):
        run = []
        for i, s in enumerate(frames):
            name = f'{chr(97 + p)}{i:02d}.jpg'; im = Image.open(SRC / f'f{s:06d}_s.jpg').convert('RGB')
            im.resize((width, round(width*im.height/im.width)), Image.LANCZOS).save(DEST / name, quality=q, optimize=True, progressive=True); run.append(name)
        runs.append(run)
    prompts = []
    for s in walk:
        p = log.get(s, {}).get('prompt')
        if p and p not in prompts: prompts.append(p)
    (DEST / 'index.json').write_text(json.dumps({'every': a.every, 'runs': runs, 'made': datetime.date.today().isoformat(),
        'from': f'frames {walk[0]} to {walk[-1]} of one walk of the spring (code/sink.py), one in every {step}',
        'prompts': prompts, 'frames_without_a_logged_prompt': sum(1 for f in picks for s in f if s not in log),
        'note': 'no frame was dreamed with a face at the sink'}, indent=1) + '\n')
    return sum(f.stat().st_size for f in DEST.iterdir())
width, q = a.width, 84; total = pack(width, q)
while total > a.budget:                                  # walk the quality down, then the width, until it fits
    if q > 56: q -= 4
    else: width = round(width*0.88/16)*16
    total = pack(width, q)
print(f'wrote {DEST}: {a.passages} passages of {a.frames} frames, frames {walk[0]} to {walk[-1]} one in every {step}, {width} px wide, quality {q}, {total} bytes ({total/1e6:.2f} MB)')
print('frames without a logged prompt:', sum(1 for f in picks for s in f if s not in log), 'of', need)
