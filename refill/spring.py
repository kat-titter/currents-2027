#!/usr/bin/env python3
# The spring's own, as the refill needs it: the prompt grammar, the sizes and strengths of a dream, and the grade. Copied word for
# word from the spring of vanitas_veritas (kat-titter/vanitas-veritas at 4308e51: code/sink.py and code/harmonize.py), so this piece
# can change its words and its colour here without touching that one. latent.py beside this file is that repo's code/latent.py, whole.
import itertools, math, random, re
import numpy as np
from PIL import Image

# ---- sizes and strengths (code/sink.py)
W, H, STEPS, GUID = 640, 480, 10, 1.5                   # frame size; LCM steps of a dream; guidance
DREAM_S = (.34, .44)                                   # how hard a dream pulls toward its words: the subject just surfaces, barely clear (uncanny)
WORDS_MIX = (.08, .25)                                 # each dream's words lie between two prompts, the second a trace: a continuum, the first still names it
WP_F, WP_STR, WP_STEPS = (.25, .5, .75), (.40, .46, .40), 8   # waypoints: where on the way; how hard; steps

# ---- the words (code/sink.py)
CORE = ['flower', 'flower in bloom', 'peony', 'daisy', 'skull', 'soap bubble', 'a face, eyes closed', 'a face in profile']   # hers
NOTES = ['pearls', 'a moth', 'an hourglass', 'a glass bottle', 'smoke from a snuffed candle', 'hands under running water',   # at most one
         'a pocket watch', 'a cracked egg', 'a wilting tulip', 'an oyster shell', 'a butterfly', 'a feather', 'a glass of water',
         'a hand mirror', 'a seashell', 'a peeled lemon', 'falling petals', 'a dragonfly', 'melting ice', 'a bee', 'a lit candle',
         'a broken string of pearls', 'spilled wine', 'a snail', 'a burnt match', 'a key', 'a cut pomegranate', 'a sparrow',
         'a wristwatch', 'a fallen petal', 'a cracked mirror', 'a coin', 'a dried rose', 'a glass marble', 'a silk ribbon', 'a wasp nest']
MOODS = ['dissolving into light', 'blooming', 'about to burst', 'half erased', 'in a long exposure', 'melting slowly',
         'scattering into dust', 'reflected in glass', 'drifting apart', 'holding still', 'breathing in', 'caught in a current',
         'fading at the edges', 'rising like steam', 'under water', 'just before waking', 'unravelling', 'turning to glass',
         'coming into focus', 'in slow motion', 'frozen mid-air', 'cracking open', 'pooling', 'overflowing', 'surfacing',
         'losing its color', 'asleep', 'weightless']
LIGHT = ['', 'in moonlight', 'at first light', 'in a single shaft of light', 'backlit', 'in the dark', 'by candlelight',
         'in cold light', 'in silver light', 'through rain', 'in a mirror', 'at dusk', 'in the last light',
         'lit from below', 'in lamplight', 'in a long shadow', 'through frosted glass', 'by a window']        # often none
STYLE = ('silver gelatin photograph, hard light, crisp point cloud of white dots, a few tiny copper sparks, '
         'vertical glitch streaks, deep black background, high contrast, film grain')
NEG = ('text, watermark, signature, frame, border, grid, colorful, pastel, cartoon, illustration, painting, blurry, soft glow, haze, '
       'fog, blue tint, sepia, washed out, low contrast, deformed hands, extra fingers, gold ball')
STATUE = ('a smooth white marble statue of a face, eyes closed, serene, a fine mesh of depth points across the head, polished stone, '
          'clean edges')                               # a face at the sink, dreamed as a statue: their likeness, made smooth and still
NEG_FACE = ', rough, noisy, blotchy, smeared, broken edges, deformed, ugly'
GLASS = {'soap bubble': 'clear glass soap bubble'}       # her bubbles are clear glass with a few sparks; the model makes gold balls

def prompts(state):
    """Functionally endless prompts: three subjects (hers, at most one other vanitas object), in an order, a mood and sometimes a
    light. The space is walked by a stride that visits every prompt once, in a scrambled order, without storing it; the place in
    it survives a restart. At a dream every two minutes it would take years to come round."""
    trios = [c for c in itertools.combinations(CORE + NOTES, 3) if sum(x in NOTES for x in c) <= 1
             and any(x in c for x in ('skull', 'soap bubble')) and any(x in c for x in CORE[:4] + ['skull'])]
    orders = list(itertools.permutations(range(3)))
    N = len(trios)*len(orders)*len(MOODS)*len(LIGHT)
    def stride(r):                                      # a step coprime to N: i -> (a*i + b) % N visits every index once
        a = r.randrange(N//3, N) | 1
        while math.gcd(a, N) != 1: a += 2
        return a, r.randrange(N)
    if 'stride' not in state:                           # each life draws its own walk from the machine's entropy, kept so a restart
        state['stride'] = stride(random.Random(state.get('life', 7)) if state.get('i') else random.SystemRandom())   # never repeats a prompt
    if state.get('N', N) != N: state['stride'] = stride(random.SystemRandom())   # the grammar changed: a new walk that fits it
    state['N'] = N
    a, b = state['stride']
    while True:
        if state['i'] and state['i'] % N == 0:
            state['life'] = state.get('life', 7) + 1; state['stride'] = stride(random.SystemRandom()); a, b = state['stride']
        x = (a*(state['i'] % N) + b) % N; state['i'] += 1
        x, li = divmod(x, len(LIGHT)); x, mi = divmod(x, len(MOODS)); ti, oi = divmod(x, len(orders))
        c = [trios[ti][j] for j in orders[oi]]; m = MOODS[mi] + (' ' + LIGHT[li] if LIGHT[li] else '')
        yield f"vanitas [{', '.join(c)}], {m}", f"vanitas, {', '.join(GLASS.get(y, y) for y in c)}, {m}, {STYLE}"

def sd_prompt(words):
    """Midjourney's words in the dream's own grammar: vanitas [a, b] becomes vanitas, a, b, and the style."""
    w = re.sub(r'(\s*[,\[\]]\s*)+', ', ', words).strip(' ,') or 'vanitas'
    for a, b in GLASS.items(): w = w.replace(a, b)
    return w + ', ' + STYLE

# ---- the grade (code/harmonize.py)
COOL       = (0.93, 0.98, 1.09)   # cool/blue tint of the monochrome base
GOLD_TONE  = (1.22, 0.80, 0.30)   # goldish-orange for warm accents
WARM_SCALE = 40.0                 # source R-B above this => full gold accent
CONTRAST   = 1.30                 # S-curve steepness (>1 = more contrast)
BLACK_GAMMA= 1.18                 # deepen blacks
GAIN       = 1.05

def harmonize(img):
    x=np.asarray(img.convert("RGB"),np.float32)
    warm=np.clip((x[...,0:1]-x[...,2:3])/WARM_SCALE,0,1)          # source warmth -> gold mask
    lum=0.299*x[...,0:1]+0.587*x[...,1:2]+0.114*x[...,2:3]
    x=(1-warm)*(lum*np.array(COOL))+warm*(lum*np.array(GOLD_TONE))# cool base + gold accent
    n=np.clip(x/255,0,1)
    n=1/(1+np.exp(-CONTRAST*4*(n-0.5)))                          # contrast S-curve
    n=n**BLACK_GAMMA*GAIN                                         # deepen blacks
    return Image.fromarray(np.clip(n,0,1).astype(np.float32).__mul__(255).astype(np.uint8))

# ---- [syn[k]]hole's own (2026-11-17; its art direction: gold, copper and brass out, a pearlescent sheen in). Above is the shared
# spring as it was copied; here this piece departs from it, and Vanitas Veritas keeps its gold. The warm accent the grade made gold
# takes a pearl tone (near white, a breath of rose and blue), the copper sparks in the words become pearl glints, and the metals join
# the negative. harmonize() and the prompts read these names when they run, so the grade and the words follow.
GOLD_TONE = (1.05, 0.98, 1.04)            # was (1.22, 0.80, 0.30): gold
STYLE = STYLE.replace('a few tiny copper sparks', 'a few tiny pearl glints')
NEG += ', gold, copper, brass, orange'
# Kat, 2026-11-17: the two face subjects cut. To put them back, delete the next line.
CORE = [c for c in CORE if c not in ('a face, eyes closed', 'a face in profile')]
