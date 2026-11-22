# currents-2027

Kat Titterton's work for CURRENTS 2027, Santa Fe.

- [s[i/y]n[k][w]hole: https://kat-titter.github.io/currents-2027/synkhole/
- about the piece: https://kat-titter.github.io/currents-2027/synkhole/about.html

By Kat Titterton (macrofluidic). An evolution of Vanitas Veritas, an earlier sink, which keeps its own address: https://kat-titter.github.io/veritas/

## What it is

A proposed installation: a sink without water. In its basin a screen pours a machine's dream as water, and one heart beats in it. At the link that heart is printed 48 times, as Warhol printed Marilyn; one number, turned across the copies, takes a steady beat into chaos. Every day the water runs out.

It began at a sink. At Room Service, a party in Tahoe, in November 2026, Kat was thirsty and could not find a cup, so she put her head under the bathroom tap and drank while strangers took turns behind her. Nobody asked whose water it was. The piece asks the same of AI, which drinks real water mostly where nobody sees it, and of Santa Fe, a city in a desert.

It grows out of Kat's [Vanitas Veritas](https://kat-titter.github.io/veritas/) (2026), a gold sink: eight of her Midjourney still lifes melting into each other through the same diffusion model, poured into a basin you could hold still. Asked what it would be in Santa Fe, the gold drained out, the one basin became 48 copies of one heart, and the water became something a desert counts.

## A creative eval

The piece is also an experiment: how much of a work of art can AI make, and how much must a person still bring?

- **Made by machines:** the water (Stable Diffusion 1.5 with LCM-LoRA, walking toward eight pictures Kat chose in Midjourney; Real-ESRGAN for detail), and, with Claude (Anthropic) through [Claude Code](https://claude.com/claude-code), the code and the first drafts of the texts, over many sessions.
- **Made by Kat:** the taste, the message, the story at the sink, and every keep or cut. She was the human in the loop the whole way.

The [about page](https://kat-titter.github.io/currents-2027/synkhole/about.html) marks each step of the making as AI, AI-assisted or not AI.

## Sources the about page cites

Indra's net, as drawn in Mumford, Series and Wright's *Indra's Pearls*; Warhol's *Marilyn Diptych* (1962); Li et al. on AI's water use, [arXiv:2304.03271](https://arxiv.org/abs/2304.03271); Ho, Jain and Abbeel's diffusion models, [arXiv:2006.11239](https://arxiv.org/abs/2006.11239); Steve Reich's 1967 note on *Piano Phase*; Siddhartha Mukherjee's *The Song of the Cell*; Scholkmann, Zohdi and Wolf on heartbeats per breath, doi:10.33549/physiolres.934232.

## The repository

- `src/`: the source of the piece and its about page; `python3 src/deploy.py` builds them into `synkhole/`. Never published.
- `synkhole/`: the built pages, with `doc/` (the about page's pictures) and `reservoir/` (stored dreams, from `src/reservoir.py` or the refill).
- `refill/`: dreams new water on a runner (`.github/workflows/refill.yml`).
- `src/archive/`: three versions of the piece from 17 Nov and the script that built them, retired.
