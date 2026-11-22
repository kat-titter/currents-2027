# [s[i/y][k][w]hole: progress

## 2026-11-21: about page truth pass for the grid (branch `about-truth`)

Kat: "the about page seems like it's out of date ... honest, accurate, transparent with the methods. Show don't tell ... true with capital T's."
Every claim on `src/about.html` checked against `src/index.html` at main `e522104` (line numbers below are that file's; main `20a01d4` since removed the hover label and the soft glow, rows 6 and 36) and the spring's
`code/sink.py` (outside this repo). T = true, S = stale (true of the single basin or of an older plan, not of the grid), F = false now.

### What a visitor gets: stored water, not a live stream

The published piece pours **stored dreams only**. The spring (`code/sink.py`, Stable Diffusion 1.5 + LCM-LoRA on Kat's laptop) is not running,
and the address its pointer names (`vanitas-veritas/verse/spring.json`, a trycloudflare tunnel) does not answer. The refill workflow is off
(`REFILL_EVERY=off`; scheduled runs skip). So the page pours `synkhole/reservoir/`: 60 frames, 6 passages of 10, one in every 2 frames of
one walk (frames 37368 to 37487), made 2026-11-17, 5 s apart, passages in a fresh order each visit (`index.html:689-712`, `reservoir/index.json`).
The live site serves the same `index.json`. The code would still let a woken spring take the tap back (`index.html:60-62, 664-683`); the page says that, no more.

### Claims

| # | Section: claim | Was | Settled by | Page now |
|---|---|---|---|---|
| 1 | hero: "a machine dreams the water" | S | stored frames (`:692`) | "the water is a machine's dream" |
| 2 | hero / thesis: every day it runs dry; one water, one heart, every copy a little off | T | thirst `:957-963`, `GRID_N` `:951` | kept |
| 3 | 01: one heart printed 48 times; one number steps it from steady through doubling into chaos | T | `GRID_RS` `:951`, `gridAssign` `:979` | kept |
| 4 | 01: "once each morning of the festival, it fills. every hand in this room spends it" | F | `dryAt` uses the clock only (`:963`, `:1066`); no hand term | fills at 6 am Santa Fe; wildest dry by late afternoon, steadiest just before dawn, watched or not |
| 5 | 01: SD 1.5 + LCM-LoRA "dreams the water live on its own computer" | F | spring off; reservoir `:692-712` | "dreamed this water on my laptop ... what pours now was stored on 17 nov 2026" |
| 6 | 02 note 1a: bubbles "swell slowly, shine, and pop" | F | nacre finish `:481-485, 512-517, 528` (e522104); whole dots, no soft glow (20a01d4) | nacre, no shine, each dot whole and one flat film colour, in rings, rim in shadow |
| 7 | 02: "2.5 s between frames" | F | `reservoir/index.json` every 5; sink.py CAD 2.5-3.5 s | "5 s between stored frames" |
| 8 | 02: "48 copies of one heart" | T | `:951` | kept |
| 9 | 02: a dot is "as large as its patch of water is bright" | S | in the grid also as the last ring's beat value: `korb` `:558-562` | "size = light × beat"; dots as bright and as the last heartbeat that rolled past |
| 10 | 02: near the hole "every dot's clock runs slow, then stops" (+ clocks figure 1, ½, ¼, ⅛, 0) | S | `bhClock` `:494` still computed, but in the grid it shows as colour (`:529`) and letters (`:520`); the note-value stepping (`tw8` tick, `:504-507`) is replaced by `korb` | clock shown as colour: rose, dim, a letter; figure redrawn from the shader's formula, caption `clock = √(1 − edge/r)` |
| 11 | 02 note 2: slower near the drain, and rose | S | as 10 | "the dots keep that clock and show it as colour" |
| 12 | 02 note 2a: no warm colours, gold went grey | T | `kw:'1'` in LOOK `:54`, `:82` | kept |
| 13 | 02 caption `water = dream()` | S | the line the code writes now is `RES_LINE` `:692` | `water = reservoir.pour()  # stored dreams: the spring is asleep` |
| 14 | 02: tap a copy to fall in, tap again to climb out; press and hold to reach the shared water | T | `gridTap` `:999-1005`, `gridSim` `:998` | kept; added "the same patch moves in all 48" |
| 15 | 02: "for about a second it follows your hand" | T~ | `grip = exp(-held/1.7 s)` `:1095` | caption `grip = exp(−held/1.7 s)` |
| 16 | (missing) the hand's gravity | — | `uHG` `:487-489`, `:1200-1202` | "the dots lean toward your hand as toward a small hole" |
| 17 | 03: "one allocation of dreaming per morning, ten mornings ... every hand opens the tap ... drains to black in under a minute" | F | thirst on the clock `:957-963`; no hand spend; the drain to black runs only if no water arrives at all (`:1083-1088`) | one water a day for all 48, turning at 6 am Santa Fe; chaos drinks most, pace a little; on the copy's beat, in patches |
| 18 | 03: ten-mornings figure (11 to 20 June) | F | as 17 | redrawn: the 48 copies at 6 am, 10 am, 2 pm, 6 pm, 10 pm, 2 am, from the piece's own formula; caption `thirst = 0.85*chaos + 0.15*pace` (`:980`) |
| 19 | 03: water axis 1.00 to None (drain to black) | S | as 17 | one copy drying in patches, axis `dry` 0 to 1, dry dots leave grid points and bracket-word letters (`:566-568`) |
| 20 | 03: "come late and you'll know who spent it" | F | nobody spends it | "come late and the wild copies are already spelling" |
| 21 | 03: "proposed. only the drain is built so far." | F | thirst is built | "hands do not spend it. time does." |
| 22 | 03: 700,000 l; 4.2 to 6.6 billion m³ (Li et al.) | T | arXiv:2304.03271 abstract, read 2026-11-21 | kept |
| 23 | 04: eight Midjourney pictures; 44 subjects, 28 moods, 18 lights | T | sink.py `CORE`+`NOTES` 44, `MOODS` 28, `LIGHT` 18; `source/moodboard/` 8 files | kept |
| 24 | 04: "3 of 10 steps follow the prompt" | T~ | sink.py `STEPS=10`, `DREAM_S=(.34,.44)` | "3 or 4 of 10" |
| 25 | 04: walk; real-esrgan four times larger | T | sink.py header (640×480 to 2560×1920) | kept |
| 26 | 04: (missing) the stored water, the print, thirst | — | `:689-712`, `:947-963` | steps added: store, print, thirst; water "in your browser" |
| 27 | 05: k = 0.25; the six moves (hole in the hole, time stutters, clear on the way out, lost line, face, lens) | T | `k:'0.25'`, `kn`, `kf` in LOOK `:54`; `kOn` `:84`; grid draws each copy with them `:1206, 1016-1029` | kept |
| 28 | 05: "the rim says how long it stayed" | S | the lost line circles the screen's centre at the single basin's drain size (`kRimDraw` `:863-868`), not a copy's drain | "a ring of small type says how long it stayed" |
| 29 | 05: lens "their clocks slowing to a stop" | S | as 10 | "inside it, the basin again, upside down" (`:491`) |
| 30 | 06: "dots, rings, bubbles, glyphs and the twist all step on one heart" | S | each copy has its own heart (`hBeat` `:931-946`); bubbles answer the water's heart `kq` (`:1143`) | "each copy ... steps on that copy's heart. the bubbles keep the water's own." |
| 31 | 06 score: dots ½ ¼ ⅛ rows | F | as 10 | rows now heart, rings, glyphs, twist, thirst, bubbles |
| 32 | 06: "near the hole a dot's clock slows to half time, a quarter, an eighth: note values" | F | as 10 | replaced by the rings: steady = one size, doubling = two, chaos = none alike (+ new rings figure, r = 2.9, 3.2, 3.83, 4.0) |
| 33 | 06: crests at 1.5× ring speed; phrase of 32, every fourth quiet | T | ripples `:543-545` (0.195 vs 0.13); `h.ba` `:937` | kept |
| 34 | 06: Warhol 50 Marilyns, 1962 | T | Tate record (linked) | kept |
| 35 | 06: "across, r climbs ...; down, the pace quickens 6%" | S | r runs along the longer side, pace the shorter (`gridAssign` `:976-981`); on a phone that is down | "along the long side ... along the short side"; added r's wander ±0.006 (`:1066`) |
| 36 | 06: "today's heart down the middle" | S | grid runs r 2.9 to 4.0; shared numbers hz 0.9, ripple 0.13, touch 0.2, hole 0.046 hold for all | "down the middle, the numbers the piece runs, with r at 3.71"; the hover label is gone from the piece (main `20a01d4`, Kat: "no hover to reveal paramaters. desribe the axis in the about page"), so a new axes figure names both axes: r 2.9 to 4.0 along the long side with each copy's loop (1, 2, 4, 8, never, 3, never), pace 0.97 to 1.03 along the short (`gridAssign`) |
| 37 | 06 prints, touch: "letting go lifts it 10%" | F | `kq.touch=0.7` on release, `tq` peaks ≈ 0.51, ×(1 + 0.3 tq) ≈ +15% (`:815, 908, 931`) | 15% |
| 38 | 06: "below 3.57 ... a loop two, four, eight beats long" | T~ | logistic map; below r = 3 one steady gap | "below r = 3 one steady gap; past it two, four, eight" |
| 39 | 06: "a hair apart ... within about 12 beats" at 3.71 | T if a hair = 0.001 | simulated: median 12 beats for 0.001, 18 for 0.0001 | "a thousandth apart" |
| 40 | 06: "across its width, in eight steps from 2.9 to 4.0" | S | 8 columns only on a wide screen; interpolated otherwise (`gridR` `:952`) | "along its long side, from 2.9 to 4.0, through 3.71 and the window of three at 3.83" |
| 41 | 07: lineage marks (built / not built) | T | lag `kLate`, memory `km`, grid, sync concepts | kept |
| 42 | 08: silent, no camera or microphone, no real water, keeps nothing of you | T | `solo` in LOOK: no relays (`:720`); no `camera` flag | kept |
| 43 | 08 timeline: "daily budget" proposed | F | thirst built; hand-spent budget not in the code | built: 48 copies, thirst; proposed: basin on its plinth |
| 44 | 09: "within 40 seconds the page notices and pours stored dreams instead" | S | true mechanism (`STALE` `:646` = 40 s at 5 s frames), but the spring has slept since 17 Nov | "it has slept since 17 nov 2026, so the page pours what it stored that day ... wake the spring and it takes the tap back" |
| 45 | glossary: "when the basin runs dry, its dots spell these" | F | the dry line is `GX_WORDS` (`:118`), 8 of the 13 entries | "a dry copy's dots spell `[s]ink [d]rain s[pace] [k]now [c]lock [h]old pe[a]rl [w]hole`" |
| 46 | small drawn marks (01 basin, 08 plan, 06 prints, hand, pictures) stepped dots at half/quarter/eighth time near the hole | S | as 10 | they step once a beat; the slow clock stays as rose |

### Follow-ups for the piece (index.html, not touched here)

- The thirst's dawn is fixed at 13:00 UTC (`:960`): 6 am in Santa Fe in winter, 7 am in June (MDT). The page says "six each morning, santa fe time", true now.
- In the grid, the `lost = mm:ss` ring (`kRimDraw`) circles the screen's centre at the single basin's drain size, between copies.

### Check

`check-page.sh synkhole/about.html` at 1280 and 400 px, light and dark: no overlap, no sideways scroll, no clipped text, no contrast failure
outside the pearl gradient words (`.h`, `.k`, transparent text the checker reads as ratio 1, as before this pass). One tiny run fixed
(the glossary's code line, 8.7 px, now 12 px).
