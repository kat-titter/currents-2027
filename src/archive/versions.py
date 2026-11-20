#!/usr/bin/env python3
"""Build the versions of [syn[k]]hole beside the piece: synkhole/v1.html, v2.html, v3.html, each from index.html (the staged starter) plus
one move of its own and its own defaults. index.html is read, never written. Each move is a flag in its page's LOOK, so <flag>=off on a
version's address gives back the starter exactly (the stepped-clock proof compares them).
    python3 synkhole/versions.py            writes all three; stops with nothing written if an anchor is missing
Private overnight work for Kat, 2026-11-17 (the versions session); notes in currents_2027/private/versions.md."""
import pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
SRC = (HERE / 'index.html').read_text()

def patch(text, edits):
    for at, new, how in edits:
        n = text.count(at)
        if n != 1: sys.exit(f'versions.py: anchor found {n} times, need 1: {at[:80]!r}')
        text = text.replace(at, {'swap': new, 'before': new + at, 'after': at + new}[how])
    return text

# shared by every version: its title, its LOOK, and where its own code joins the shaders and the clock
LOOK0 = "const LOOK = { k:'0.25', kn:'0.5', kf:'0.5', kb:'1', kc:'rim', km:'1', kw:'1', reservoir:'', solo:'' };"
TITLE0 = '<title>[syn[k]]hole, dry season, CURRENTS 2027</title>'
SHADERS = "  FS.display = FS.display.split('texture(uDye,').join('kdye(');"      # a version's shader lines go in just before this
CLOCK = 'const Q0 = 0.005, H = 1/SIM;'                                       # its own clock just before this
HANDS = "if (K > 0) { sg = kq.w < 0 ? -1 : 1; if (kOn('6')) { kLate(now); hs = kq.lh; st = kq.ls; gs = kq.lg; } }"   # after the hand the water feels is chosen
FORCE_U = 'gl.uniform4f(u.uGrab, hs.u, hs.v, gs, 0.06); gl.uniform2f(u.uGrabVel, hs.vx*sg, hs.vy*sg);'
DYE_U = 'gl.uniform2f(u.uTap, tap[0], tap[1]); gl.uniform4f(u.uGrab, hs.u, hs.v, gs, 0.06);'
DRAW = 'draw(null); if (mips) gl.bindSampler(0, null);'
STRENGTHS = 'const KW = K > 0 ? kNum(\'kw\', 0) : 0;   // warmth out: how much of a dream\'s gold and copper goes grey'
C_LINE = 'vec3 c = clamp(texture(uDye, p).rgb, 0., 1.);'

# ---- v1, the twin: when your hand is in, a second hand answers from across the drain, a beat late, and the dream round it is the dream round
# your hand turned half a turn. For stretches the water obeys the twin and your own hand is drawn a beat late. Let go: clear for a breath, then
# the twin comes back without you and replays what your hand did, fainter, and sinks. With no one here, it replays the last hand it held.
V1 = [
  (TITLE0, '<title>[syn[k]]hole v1, twin</title>', 'swap'),
  (LOOK0, LOOK0.replace("solo:''", "solo:'', tw:'1'") + '   // v1: tw, the twin', 'swap'),
  (STRENGTHS, "\nconst TW = K > 0 ? kNum('tw', 0) : 0;   // v1: the twin across the drain", 'after'),
  (SHADERS, """  if (TW > 0) {                                        // v1, the twin: a second palm in the water, the mirror of yours through the drain
    put('force', 'uniform vec4 uGrab;', ' uniform vec4 uTw; uniform vec2 uTwVel;');
    put('force', 'v = mix(v, uGrabVel, m*(1.-exp(-30.*uDt)));', `
  { vec2 g2 = vUv-uTw.xy; float gr2 = length(g2);        // the twin's palm: the water under it goes where the twin goes
    float f2 = mix(0.15, 1., smoothstep(0.2, 0.8, 0.5+0.5*cos(5.*atan(-g2.y, -g2.x)+0.6)));   // its fingers, turned half a turn
    float m2 = uTw.z*exp(-gr2*gr2/(uTw.w*uTw.w))*mix(1., f2, smoothstep(0.35, 0.95, gr2/uTw.w));
    v = mix(v, uTwVel, m2*(1.-exp(-30.*uDt))); }`);
    put('dye', 'uniform vec2 uTap; uniform vec4 uGrab;', ' uniform vec4 uTw;');
    put('dye', 'float held = uGrab.z*exp(-dot(g,g)/(uGrab.w*uGrab.w));', ' vec2 g2 = vUv-uTw.xy; held = max(held, uTw.z*exp(-dot(g2,g2)/(uTw.w*uTw.w)));');   // what the twin holds stops re-forming too
    put('display', 'uniform vec4 uKH;', 'uniform vec4 uTwQ; uniform vec2 uMineQ; uniform float uTwM, uTwP;   // the twin: where, how present, its grip; where your own hand is drawn; how much of the dream it mirrors\\n', 'before');
    put('display', 'vec2 hq = q-(uCursor-uCenter)/uS;', 'vec2 hq = q-uMineQ, tq2 = q-uTwQ.xy;', 'swap');
    put('display', 'float L = (1.-pool*smoothstep(0., -0.08, sd))*uGlass;', ' L *= 1. - smoothstep(0.045+0.05*uTwQ.w, 0.012, length(tq2))*uTwQ.z*smoothstep(0., -0.08, sd);   // the glass lies flat under the twin too');
    put('display', 'vec3 c = clamp(texture(uDye, p).rgb, 0., 1.);', `
    { float tr = length(tq2), ta = atan(tq2.y, tq2.x);   // round the twin the dream is the dream round your hand, turned half a turn: the same patch twice; its edge soft and never round
      float edge = (0.12 + 0.13*uTwP)*(1. + 0.32*(vnoise(vec2(ta*1.3 + 7., uTime*0.23)) - 0.5) + 0.10*sin(3.*ta + uTime*0.37));
      vec2 td = uTwQ.xy/max(length(uTwQ.xy), 1e-4);      // only on the twin's side of the drain: near the hole the two halves are each other, turned, and the basin is symmetric there
      float side = smoothstep(-0.025, 0.025, dot(ql, td) + 0.02*(vnoise(ql*11. + uTime*0.1) - 0.5));
      c = mix(c, clamp(texture(uDye, C - ql).rgb, 0., 1.), uTwM*smoothstep(edge, edge*0.3, tr)*side); }`);
    put('display', 'b += BONE*0.30*uHold*uCursorOn*exp(-pow((hr-rp)/0.0035, 2.))*mix(0.25, 1., fingers)*(0.35+0.65*uGrip); }', `
    { float hr = length(tq2), rp = 0.034+0.012*uTwQ.w;   // the twin's palm: the same bright edge as yours, its fingers turned half a turn
      float fingers = smoothstep(0.2, 0.8, 0.5+0.5*cos(5.*atan(-tq2.y, -tq2.x)+0.6));
      b += BONE*0.30*uTwQ.z*exp(-pow((hr-rp)/0.0035, 2.))*mix(0.25, 1., fingers)*(0.35+0.65*uTwQ.w);
      b *= 1. - 0.45*uTwQ.z*exp(-pow((hr-rp-0.011)/0.009, 2.))*mix(0.3, 1., fingers);   // a palm presses the surface: a soft dark meniscus outside the bright edge
      float mr = length(hq), mf = smoothstep(0.2, 0.8, 0.5+0.5*cos(5.*atan(hq.y, hq.x)+0.6));   // and the same under your own palm, so the two read alike
      b *= 1. - 0.45*uHold*uCursorOn*exp(-pow((mr-0.034-0.012*uGrip-0.011)/0.009, 2.))*mix(0.3, 1., mf); }`);
  }
""", 'before'),
  (CLOCK, """// ---- v1, the twin. tw.a how present it is, tw.g how hard it grips, tw.sw the swap (1: the water answers the twin and your hand is drawn late)
const tw = { hist:[], path:[], rp:null, was:false, a:0, g:0, sw:0, m:0, p:0, u:0.5, v:0.5, vx:0, vy:0, mu:0.5, mv:0.5 };
const TW_LATE = 0.8;                                  // a beat late, in seconds
{ const n = 120; for (let i = 0; i <= n; i++) { const f = i/n, e = f*f*(3 - 2*f);   // a hand that was here before you: a slow arc on the right, held 4 s
  tw.path.push([4000*f, 0.69 - 0.05*Math.sin(3.1*e), 0.63 - 0.27*e, 0, 0]); }
  for (let i = 1; i <= n; i++) { const a = tw.path[i - 1], b = tw.path[i], s = (b[0] - a[0])/1000; b[3] = (b[1] - a[1])/s; b[4] = (b[2] - a[2])/s; }
  tw.rp = { at:9000 }; }                              // it comes back 9 s after the page opens
function twAt(path, ms){                              // the hand on a recorded path at ms after it reached in
  let i = 0; while (i < path.length - 2 && path[i + 1][0] < ms) i++;
  const a = path[i], b = path[Math.min(i + 1, path.length - 1)], f = b[0] > a[0] ? Math.max(0, Math.min(1, (ms - a[0])/(b[0] - a[0]))) : 0;
  return [a[1] + (b[1] - a[1])*f, a[2] + (b[2] - a[2])*f, a[3] + (b[3] - a[3])*f, a[4] + (b[4] - a[4])*f];
}
function twTick(dt, now){
  tw.hist.push([now, hand.u, hand.v, hand.vx, hand.vy, hand.down ? 1 : 0, grip]);
  while (tw.hist.length > 2 && tw.hist[1][0] <= now - TW_LATE*1000) tw.hist.shift();
  const L = tw.hist[0];                               // your hand a beat ago
  if (hand.down && !tw.was) { tw.path = []; tw.rp = null; }
  if (!hand.down && tw.was && tw.path.length > 20) tw.rp = { at:now + 4500 };   // let go: after the clear breath, the twin comes back without you
  tw.was = hand.down;
  let a = 0, g = 0, sw = 0, src = null;
  if (hand.down) {
    const held = (now - hand.t0)/1000, x = held % 9;  // held 2.5 s, then for 4 s in every 9 the water answers the twin
    if (tw.path.length < 400 && (!tw.path.length || now - hand.t0 - tw.path[tw.path.length - 1][0] > 33)) tw.path.push([now - hand.t0, hand.u, hand.v, hand.vx, hand.vy]);
    sw = held > 2 ? kss(2.5, 3.5, x)*(1 - kss(6, 7, x)) : 0;
    a = L[5] ? 1 : 0; g = 0.45*L[6] + 0.7*tw.sw; }
  tw.sw += (sw - tw.sw)*(1 - Math.exp(-dt/0.25));
  if (hand.down) { const f = tw.sw; src = [L[1] + (hand.u - L[1])*f, L[2] + (hand.v - L[2])*f, L[3] + (hand.vx - L[3])*f, L[4] + (hand.vy - L[4])*f];
    tw.mu = hand.u + (L[1] - hand.u)*f; tw.mv = hand.v + (L[2] - hand.v)*f; }   // in the swap the twin is on time and your own hand is the late one
  else { tw.mu = hand.u; tw.mv = hand.v;
    if (tw.rp && now >= tw.rp.at && tw.path.length > 1) {   // the replay: twice, fainter, then it sinks into the drain
      const dur = tw.path[tw.path.length - 1][0]/1000 + 1.2, e = (now - tw.rp.at)/1000, n = Math.floor(e/dur), pos = (e - n*dur)*1000;
      if (n < 2) { const s = twAt(tw.path, pos), fade = kss(0, 0.6, pos/1000)*(1 - kss(dur - 1.4, dur - 0.6, pos/1000)); src = s; a = (n ? 0.5 : 0.85)*fade; g = 0.55*a; }
      else { const k = Math.min(1, (e - 2*dur)/3.5), s = twAt(tw.path, 0), du = 0.5 - s[0], dv = 0.5 - s[1], r = Math.pow(1 - k, 1.6), th = 2.6*k;   // it sinks: round the drain and into it
        const ru = (du*Math.cos(th) - dv*Math.sin(th))*r, rv = (du*Math.sin(th) + dv*Math.cos(th))*r;
        src = [0.5 - ru, 0.5 - rv, 0, 0]; a = 0.5*(1 - kss(0.5, 1, k)); g = 0.4*a;
        if (k >= 1) tw.rp = { at:now + 45000 }; } } }   // with no one here, the last hand comes back every 45 s
  if (src) { tw.u = 1 - src[0]; tw.v = 1 - src[1]; tw.vx = -src[2]; tw.vy = -src[3]; }   // the mirror through the drain: where, and moving the other way
  const show = 1 - kq.clear;                          // in the clear breath it is not there
  tw.a += (a*show - tw.a)*(1 - Math.exp(-dt/0.3)); tw.g = g*show; tw.m = tw.a*(hand.down ? 1 : 0.7);
  tw.p += ((hand.down ? kss(0.26, 0.06, Math.hypot(hand.u - 0.5, hand.v - 0.5)) : 0) - tw.p)*(1 - Math.exp(-dt/0.4));   // near the drain the mirror zone widens
}
window.__tw = tw;
""", 'before'),
  (HANDS, ' if (TW > 0) { twTick(dt, now); gs *= 1 - 0.85*tw.sw; }   // v1: in the swap your own grip lets go', 'after'),
  (FORCE_U, ' if (TW > 0) { gl.uniform4f(u.uTw, tw.u, tw.v, tw.g*tw.a, 0.06); gl.uniform2f(u.uTwVel, tw.vx*sg, tw.vy*sg); }', 'after'),
  (DYE_U, ' if (TW > 0) gl.uniform4f(u.uTw, tw.u, tw.v, tw.g*tw.a, 0.06);', 'after'),
  (DRAW, 'if (TW > 0) { gl.uniform4f(u.uTwQ, tw.u - 0.5, tw.v - 0.5, tw.a, tw.g); gl.uniform2f(u.uMineQ, tw.mu - 0.5, tw.mv - 0.5); gl.uniform1f(u.uTwM, tw.m); gl.uniform1f(u.uTwP, tw.p); }\n  ', 'before'),
]

# ---- v2, grain: the generator made visible. The picture is laid on the grid it was dreamed in (64 by 48, the latent of a 512 by 384 dream);
# toward the drain, under a hand that stays, and everywhere as the basin drains, it comes apart cell by cell into the noise it was dreamed from,
# re-rolled in steps on the water's own clock (in sync with the drain's beat; stalled when time stalls). At the tap it is dreamed back. Let go: clear.
V2 = [
  (TITLE0, '<title>[syn[k]]hole v2, grain</title>', 'swap'),
  (LOOK0, LOOK0.replace("solo:''", "solo:'', gn:'1', gx:'1'") + '   // v2: gn, the grain; gx, the code in it (gx=off: grain without code)', 'swap'),
  (STRENGTHS, "\nconst GN = K > 0 ? kNum('gn', 0) : 0;   // v2: the picture comes apart into the noise it was dreamed from\nconst GX = GN > 0 ? kNum('gx', 0) : 0;   // v2: where it has gone all the way, the code line it was dreamed from", 'after'),
  (SHADERS, """  if (GN > 0) {                                        // v2, grain
    put('display', 'uniform vec4 uKH;', 'uniform vec4 uGN, uGH; uniform float uGT, uGL;   // the step, the drain\\'s reach, all of it, the clear breath; the hand: where, how much, how wide; the tap; the cell\\'s mip level\\n', 'before');
    put('display', 'uniform vec4 uKH;', 'uniform sampler2D uGA; uniform vec4 uGC[48]; uniform vec3 uGX;   // the glyph atlas; the code line, one glyph slot per character; its length, the atlas\\'s mip level, how much code\\n', 'before');
    put('display', 'vec3 c = clamp(texture(uDye, p).rgb, 0., 1.);', `
    { vec2 gp = (ql + B)/(2.*B)*vec2(64., 48.), gc = floor(gp), gf = fract(gp);   // the dream's own grid: 64 by 48, the latent a 512 by 384 picture is dreamed in
      float rd = length(ql), rh = length(q - uGH.xy), hc = hash(gc + 0.37);
      float sg = smoothstep(uGN.y, 0.032, rd) + uGN.z;                                    // the drain takes it apart; drained, the whole basin
      sg += uGH.z*smoothstep(uGH.w, uGH.w*0.25, rh*(1. + 0.4*(vnoise(gc*0.21 + 3.) - 0.5)));   // and so does a hand that stays
      vec2 tq = q - uTapQ; sg += 0.55*exp(-dot(tq, tq)/0.0007)*uGT;                         // at the tap it is dreamed from noise
      float on = smoothstep(hc*0.6, hc*0.6 + 0.4, clamp(sg, 0., 1.)*(1. - uGN.w));          // cell by cell, not all at once
      if (on > 0.001) {
        vec3 cq = clamp(textureLod(uDye, C - B + (gc + 0.5)/vec2(64., 48.)*2.*B, uGL).rgb, 0., 1.);   // the cell's own colour
        float s = uGN.x;                                                                  // which step of the few the generator takes
        vec3 e = vec3(hash(gc + s*17.13), hash(gc + s*29.71 + 5.3), hash(gc + s*41.37 + 9.1)) + vec3(hash(gc*1.7 + s*7.7), hash(gc*1.3 + s*3.1 + 2.), hash(gc*1.9 + s*5.3 + 4.)) - 1.;   // noise, near normal, per cell and step
        e = vec3(dot(e, vec3(0.333))) + 0.30*(kiri(hash(gc + s*3.7))*0.8 - 0.55);            // pearl, not rainbow: grey noise with a film's tint (cyan, violet, rose)
        float ab = 1. - on;                                                               // how much picture is left
        vec3 x0 = mix(c, cq, smoothstep(0., 0.3, on));                                     // the fine detail goes first, then the shapes
        vec3 xt = sqrt(ab)*x0 + (1. - sqrt(ab))*vec3(lum(cq)) + sqrt(1. - ab)*0.36*e;
        float edge = smoothstep(0., 0.08, min(min(gf.x, gf.y), min(1. - gf.x, 1. - gf.y)));   // where the picture has gone, its grid shows
        c = clamp(xt*mix(1., 0.88 + 0.12*edge, on), 0., 1.);
        float gg = smoothstep(0.82, 1., on)*smoothstep(0.35, 0.7, clamp(sg, 0., 1.)*(1. - uGN.w))*uGX.z;   // where a cell has gone all the way, and the pull is strong, it shows the code it was dreamed from
        if (gg > 0.) {
          float n = uGX.x, ix = mod(gc.x + floor(hash(vec2(gc.y, s) + 0.71)*n), n);        // each row reads the line from its own place, re-rolled each step
          int i = int(ix); float ch = uGC[i/4][i - 4*(i/4)];                               // which glyph: printable ASCII from slot 0, a dot for the rest
          vec3 gl3 = textureLod(uGA, (vec2(mod(ch, 16.), 5. - floor(ch/16.)) + gf)/vec2(16., 6.), uGX.y).rgb;   // pale bone on black
          gl3 *= mix(vec3(1.), kiri(hc + s*0.13)*1.15, 0.16);                              // under a thin film, pearl
          float ga = clamp(gl3.g*1.15, 0., 1.);
          c = mix(c, (0.40*cq + 0.16*xt)*(1. - ga) + 0.92*gl3, gg);                         // the cell's own colour, faint, behind
        }
      } }`);
  }
""", 'before'),
  (CLOCK, """// ---- v2, grain. gn.seed: which step of noise; it moves on the water's clock, at the drain's beat while it drains
const gn = { ph:0, seed:0, hr:0.04, ha:0 };
function gnTick(dt, now){
  const hz = 1.5 + (kOn('3') ? 1.5*Math.min(1, drainAmt/0.6) : 0);   // 1.5 steps a second; draining, up to 3, with the beat
  gn.ph += dt*Math.abs(kq.w)*hz; gn.seed = Math.floor(gn.ph) % 991;  // when time stalls, so does the generator; when it skips, the noise skips
  const held = hand.down ? (now - hand.t0)/1000 : 0;
  if (hand.down) gn.hr = 0.04 + 0.19*(1 - Math.exp(-held/5));        // the longer a hand stays, the wider the noise round it
  gn.ha += ((hand.down ? kss(0.3, 1.5, held) : 0) - gn.ha)*(1 - Math.exp(-dt/(hand.down ? 0.4 : 0.12)));
}
// the code inside the grain: where a cell has gone all the way to noise it shows one glyph of the page's own code line, read along its row
gn.tex = (() => {                       // the glyph atlas, made once: printable ASCII and a dot, 16 by 6 slots of 32 px, the page's mono font, pale bone on black
  const P = 32, cv = document.createElement('canvas'); cv.width = 16*P; cv.height = 6*P;
  const x = cv.getContext('2d'); x.fillStyle = '#000'; x.fillRect(0, 0, cv.width, cv.height);
  x.font = `${Math.round(P*0.7)}px ${getComputedStyle(document.documentElement).getPropertyValue('--mono')}`;
  x.fillStyle = '#e4dfd2'; x.textAlign = 'center'; x.textBaseline = 'middle';
  for (let i = 0; i < 96; i++) x.fillText(i < 95 ? String.fromCharCode(32 + i) : '·', (i % 16 + 0.5)*P, (Math.floor(i/16) + 0.55)*P);
  const t = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, t); gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
  gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA8, gl.RGBA, gl.UNSIGNED_BYTE, cv); gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, false); gl.generateMipmap(gl.TEXTURE_2D);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
  return t; })();
gn.codes = new Float32Array(192); gn.n = 1; gn.line = '';
function gnLine(){                      // the line as the page writes it: the prompt, the reservoir pouring (without its comment), or water = None
  const t = water > 0.5 && live.prompt ? `water = dream("${live.prompt}")` : RES && res.on && water > 0.5 ? RES_LINE.split('  #')[0] : 'water = None';
  if (t === gn.line) return; gn.line = t; gn.n = Math.max(1, Math.min(192, t.length));
  for (let i = 0; i < gn.n; i++) { const c = t.charCodeAt(i); gn.codes[i] = c >= 32 && c < 127 ? c - 32 : 95; }
}
window.__gn = gn;
""", 'before'),
  (HANDS, ' if (GN > 0) gnTick(dt, now);', 'after'),
  (DRAW, "if (GN > 0) { gl.uniform4f(u.uGN, gn.seed, 0.15, 0.85*drainAmt, kq.clear); gl.uniform4f(u.uGH, hand.u - 0.5, hand.v - 0.5, gn.ha, gn.hr); gl.uniform1f(u.uGT, water); gl.uniform1f(u.uGL, Math.log2(dye.read.w*0.92/64));\n    gnLine(); bind(u.uGA, gn.tex); gl.uniform4fv(u['uGC[0]'], gn.codes); gl.uniform3f(u.uGX, gn.n, Math.max(0, Math.log2(32/(0.92/64*view.S*view.dpr))), GX); }\n  ", 'before'),
]

# ---- v3, depth: the flat dream rises into a relief, its brightness as height, lit from the upper left; it turns as you move, the wrong way
# (higher parts slide away from you, as in a reverse perspective), and in a ring round the drain the right way: there it is inside out.
# Held, the relief steps into four flat planes, stage flats sliding on each other. Let go: flat and true for a breath. Draining, the ring spreads.
V3 = [
  (TITLE0, '<title>[syn[k]]hole v3, depth</title>', 'swap'),
  (LOOK0, LOOK0.replace("solo:''", "solo:'', dp:'1'") + '   // v3: dp, the depth', 'swap'),
  (STRENGTHS, "\nconst DP = K > 0 ? kNum('dp', 0) : 0;   // v3: the flat dream as a relief that turns the wrong way", 'after'),
  (SHADERS, """  if (DP > 0) {                                        // v3, depth
    put('display', 'uniform vec4 uKH;', 'uniform vec2 uDV; uniform vec4 uDP; uniform float uDF;   // where you look from; how deep, how lit, the ring at the drain; how flat the flats\\nfloat dFlat(float h){ return mix(h, (floor(h*4.) + smoothstep(0.30, 0.70, fract(h*4.)))/4., uDF); }   // held: four flat planes\\n', 'before');
    put('display', 'vec2 p = C+ql;', `
    if (uDP.x > 0.0002) { float rr = length(ql), sgn = mix(-1., 1., smoothstep(uDP.w + 0.035, uDP.w - 0.035, rr + 0.03*(vnoise(ql*7. + uTime*0.05) - 0.5)));   // outside the ring the relief turns the wrong way; inside it, the right way: inside out
      vec2 p0 = p; for (int i = 0; i < 6; i++) p = p0 + uDV*uDP.x*sgn*(dFlat(lum(textureLod(uDye, p, kLod + 2.5).rgb)) - 0.45); }`);
    put('display', 'c += BONE*pow(max(dot(n,Hh),0.),40.)*0.22*mix(0.4, 1., L);', `
    if (uDP.y > 0.001) { float e2 = 7./1024., l0 = kLod + 3.;    // lit as a relief from the upper left, whichever way it turns
      vec4 h4 = vec4(lum(textureLod(uDye, p - vec2(e2, 0.), l0).rgb), lum(textureLod(uDye, p + vec2(e2, 0.), l0).rgb), lum(textureLod(uDye, p - vec2(0., e2), l0).rgb), lum(textureLod(uDye, p + vec2(0., e2), l0).rgb));
      h4 = vec4(dFlat(h4.x), dFlat(h4.y), dFlat(h4.z), dFlat(h4.w));
      float lam = dot(normalize(vec3(h4.x - h4.y, h4.z - h4.w, mix(0.045, 0.16, uDF))), normalize(vec3(-0.55, 0.65, 0.52)));   // broad forms, steep: a bas-relief; held, gentler, so the flats' edges stay thin
      c *= mix(1., (0.40 + max(lam, 0.))/0.92, uDP.y); }`);
  }
""", 'before'),
  (CLOCK, """// ---- v3, depth. dp.vx, vy: where the relief is seen from (-1 to 1); it follows a hand anywhere over the basin, and rocks slowly with no one here
const dp = { vx:0, vy:0 };
function dpTick(dt){
  const tx = hand.on ? Math.max(-1, Math.min(1, (hand.u - 0.5)/BX)) : 0.8*Math.sin(simTime*0.13), ty = hand.on ? Math.max(-1, Math.min(1, (hand.v - 0.5)/BY)) : 0.65*Math.sin(simTime*0.09 + 1.3);
  dp.vx += (tx - dp.vx)*(1 - Math.exp(-dt/0.5)); dp.vy += (ty - dp.vy)*(1 - Math.exp(-dt/0.5));
}
window.__dp = dp;
""", 'before'),
  (HANDS, ' if (DP > 0) dpTick(dt);', 'after'),
  (DRAW, "if (DP > 0) { gl.uniform2f(u.uDV, dp.vx, dp.vy); gl.uniform4f(u.uDP, 0.05*DP*(1 - kq.clear)*(1 + drainAmt), 0.85*DP*(1 - kq.clear), 0, 0.10 + 0.03*Math.sin(simTime*0.21) + 0.4*drainAmt); gl.uniform1f(u.uDF, kq.soft); }\n  ", 'before'),
]

VERSIONS = {'v1': V1, 'v2': V2, 'v3': V3}
pages = {name: patch(SRC, edits) for name, edits in VERSIONS.items()}   # all anchors first, then write
for name, text in pages.items():
    (HERE / f'{name}.html').write_text(text); print('wrote', HERE / f'{name}.html', len(text), 'bytes')
