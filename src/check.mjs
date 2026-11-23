#!/usr/bin/env node
// Two checks of the piece, Node 22+, no packages: the real-time check of the page on any address (a local port, or the public one after a publish), and --thirst (the thirst schedule against the about page).
// It loads the page in a headless Chrome, lets it pour, puts a hand in, drags, lets go, and fails (exit 1) unless:
//   the water runs, the look is the default (k 0.25, no line under the basin, the code on the drain's rim), the reservoir pours when no
//   spring answers, the drag grips, the hand's time is told on the way out, and the page logged no error.
//   On the grid (?r=grid, the bare address) it checks the fall instead: a tap goes in, a drain tap falls through to depth 1, a short pull
//   slides back, a pull to the rim climbs out, a hold grips and the rim tells its time, past 30 s alone (set by __basin.idle(s)) it floats up, two fingers go out;
//   then the hearts, run 30 minutes ahead: all 48 still beating, neighbours both in step (over 0.55 of pairs) and out of it (under 0.3) at some time;
//   then the way to the about page: the corner's mass is there at rest, Enter on the unseen about link falls through it to about.html, and so does a tap in the bottom right corner.
//   On the one basin (?r=off) the link is plain: Enter on it opens about.html.
//   1. a headless Chrome:  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --remote-debugging-port=9396 \
//        --user-data-dir=<a temp folder> --window-size=960,720 --hide-scrollbars --enable-gpu --use-angle=metal --ignore-gpu-blocklist about:blank
//   2. node src/check.mjs http://127.0.0.1:8806/            the spring's water if it is awake, else the reservoir
//      node src/check.mjs "http://127.0.0.1:8806/?spring=nofeed/"     no spring: the reservoir must pour
//      node src/check.mjs "http://127.0.0.1:8806/?r=off"         the one basin: the hand in the water and the rim's lost time
//   CHECK_PORT=<port> picks another Chrome; a second argument writes a PNG of the page after the hand has left.
//   node src/check.mjs --thirst [address of synkhole/]     the thirst schedule instead. With no browser it runs index.html's thirst block (// <thirst> ... </thirst>,
//      which deploy.py also puts in the about page) and solves, second by second over the 48 ranks k/47: every clock time and count the about page quotes (each must
//      sit by its anchor words there), and the wet share, which must stay at 3/4 or more all day. With an address and the Chrome it also loads days 0.1, 0.3, 0.5,
//      0.7 and 0.9 and needs the live page to agree (__basin.thirst.wet at 3/4 or more, GL error 0, nothing logged).
import fs from 'node:fs';
const ARGS = process.argv.slice(2), THIRST = ARGS.includes('--thirst'), ABOUT = ARGS.includes('--about'), [url, png] = ARGS.filter((a) => a !== '--thirst' && a !== '--about');
const PORT = +process.env.CHECK_PORT || 9396, nap = (ms) => new Promise((r) => setTimeout(r, ms));
if (!url && !THIRST) { console.log('usage: node src/check.mjs <address> [out.png]   or   node src/check.mjs --thirst [address]'); process.exit(2); }
const fails = [], need = (ok, what) => { if (!ok) fails.push(what); };
if (THIRST) {                                                       // the about page's numbers, solved from the thirst model itself
  const read = (f) => fs.readFileSync(new URL(f, import.meta.url), 'utf8'), idx = read('index.html'), abt = read('about.html');
  const block = (idx.match(/^\/\/ <thirst>[\s\S]*?^\/\/ <\/thirst>.*$/m) || [''])[0], helpers = (idx.match(/^const kss = .*$/m) || [''])[0];   // the model, and the page's kss and kh it uses
  if (!block || !helpers) { console.log('FAIL: index.html has no // <thirst> ... // </thirst> block, or no "const kss = ..." line'); process.exit(1); }
  const { DAWN_H, dryOf } = new Function(helpers + '\n' + block + '\nreturn { DAWN_H, dryOf };')();
  const R = [...Array(48)].map((_, k) => k/47), n = (p, cut) => R.filter((r) => dryOf(r, p) > cut).length, S = 1/86400;   // a second of the day; p 0 is dawn
  const clock = (p) => { const m = Math.floor(60*DAWN_H + p*1440 + 1e-9) % 1440, h = Math.floor(m/60); return `${(h + 11) % 12 + 1}:${String(m % 60).padStart(2, '0')} ${h < 12 ? 'am' : 'pm'}`; };
  let first = null, half = null, last = null, most = 0, untouched = 48, wet = 1; const hrs = R.map(() => 0);
  for (let k = 0; k < 86400; k++) { const p = k*S, any = n(p, 0), dry = n(p, 0.5); if (any && first === null) first = p; if (dry && half === null) half = p; if (any) last = p;
    most = Math.max(most, dry); untouched = Math.min(untouched, 48 - any); wet = Math.min(wet, 1 - R.reduce((a, r) => a + dryOf(r, p), 0)/48); R.forEach((r, i) => { if (dryOf(r, p) > 0.5) hrs[i] += 24*S; }); }
  const WORD = ['zero', 'one', 'two', 'three', 'four', 'five', 'six'], lo = Math.round(Math.min(...hrs)), hi = Math.round(Math.max(...hrs)), at10 = n((10 - DAWN_H)/24, 0.5);
  const solved = { first:clock(first), firstHalfDry:clock(half), full:clock(last + S), hours:[+Math.min(...hrs).toFixed(2), +Math.max(...hrs).toFixed(2)], at10am:at10, noon:n(0.25, 0.5), six:n(0.5, 0.5), most, untouched, minWet:+wet.toFixed(3) };
  console.log('solved  ', JSON.stringify(solved));
  const esc = (t) => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), V = (v) => `(?<![\\d:.])${esc(String(v))}(?![\\d:])`;
  const near = (v, a, after) => new RegExp(after ? `${esc(a)} ${V(v)}` : `${V(v)}[^<,;.]{0,16}${esc(a)}`).test(abt);   // a value just before its anchor words (or just after), in one clause
  for (const [v, a, after] of [[solved.first, 'the dry passes'], [solved.full, 'full again'], [at10, 'dry by 10 am'], [solved.noon, 'dry at noon'], [solved.six, 'at 6 pm'], [most, 'never more than', 1],
    [untouched, 'untouched'], [`${WORD[lo]} to ${WORD[hi]}`, 'hours']]) need(near(v, a, after), `about.html has no "${v}" by "${a}"`);
  need(half <= (8.5 - DAWN_H)/24 && abt.includes('half past eight and the thirstiest copy'), `the page's "come after half past eight and the thirstiest copy" is missing or false: the first copy is half dry at ${solved.firstHalfDry}`);
  need(wet >= 0.75, `the wet share falls to ${solved.minWet} at its lowest, under 3/4`);
  if (!url) { console.log(fails.length ? 'FAIL: ' + fails.join('; ') : 'PASS: every clock time and count on the about page is the thirst model\'s, and 3/4 of the wall stays wet all day'); process.exit(fails.length ? 1 : 0); }
}
const page = (await (await fetch(`http://127.0.0.1:${PORT}/json`)).json()).find((t) => t.type === 'page');
const ws = new WebSocket(page.webSocketDebuggerUrl), wait = new Map(), errors = []; let id = 0;
await new Promise((r, j) => { ws.onopen = r; ws.onerror = () => j(new Error('no Chrome on port ' + PORT)); });
ws.onmessage = (m) => { const d = JSON.parse(m.data), p = wait.get(d.id);
  if (p) { wait.delete(d.id); d.error ? p.j(new Error(d.error.message)) : p.r(d.result); }
  else if (d.method === 'Runtime.exceptionThrown') errors.push(d.params.exceptionDetails.exception?.description || d.params.exceptionDetails.text);
  else if (d.method === 'Runtime.consoleAPICalled' && d.params.type === 'error') errors.push(d.params.args.map((a) => a.value ?? a.description).join(' '));
  else if (d.method === 'Log.entryAdded' && d.params.entry.level === 'error' && !/favicon/.test(d.params.entry.url || '')) errors.push(`${d.params.entry.text} ${d.params.entry.url || ''}`); };
const send = (method, params = {}) => new Promise((r, j) => { wait.set(++id, { r, j }); ws.send(JSON.stringify({ id, method, params })); });
const js = async (expression) => { const r = await send('Runtime.evaluate', { expression, awaitPromise:true, returnByValue:true });
  if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || r.exceptionDetails.text); return r.result.value; };
if (ABOUT) {                                                        // node src/check.mjs --about <address of about.html>: the first screen is bare, and the bar comes back once you scroll
  await send('Page.enable'); await send('Runtime.enable'); await send('Page.navigate', { url }); await nap(4000);
  const look = () => js(`JSON.stringify({ bare:document.body.classList.contains('at-top'), bar:+getComputedStyle(document.querySelector('.bar')).opacity, clock:+getComputedStyle(document.getElementById('lost')).opacity, cue:document.querySelector('.hero .cue').textContent.length, wide:document.documentElement.scrollWidth - innerWidth })`).then(JSON.parse);
  const top = await look(); await js('scrollTo(0, innerHeight), 1'); await nap(2500); const down = await look();
  console.log('about   ', JSON.stringify({ top, down }));
  need(top.bare && top.bar === 0 && top.clock === 0, `the first screen is not bare: bar ${top.bar}, clock ${top.clock}`);
  need(!down.bare && down.bar === 1 && down.clock === 1, `a screen down, the bar or the clock has not come back: bar ${down.bar}, clock ${down.clock}`);
  need(top.cue === 0 && top.wide <= 0, `the first screen carries a line of text under the title (${top.cue} characters; it shows, it does not tell), or the page is ${top.wide} px wider than the window`);
  console.log(fails.length ? 'FAIL: ' + fails.join('; ') : 'PASS: the about page opens bare and furnishes itself on scroll'); ws.close(); process.exit(fails.length ? 1 : 0);
}
const STATE = `(() => { const b = window.__basin, q = b.kq, code = document.getElementById('code'), rim = document.querySelector('svg text'), about = document.getElementById('about');
  return { water:+b.water.toFixed(3), k:b.k, grip:+b.grip.toFixed(3), soft:+q.soft.toFixed(2), clear:+q.clear.toFixed(2), lost:q.lost, clock:+q.w.toFixed(2), seq:b.seq, prompt:b.prompt.slice(0, 40),
    res:b.res, line:getComputedStyle(code).display, rim:rim ? rim.textContent : null, rimOpacity:rim ? +rim.ownerSVGElement.style.opacity : null,
    about:about ? about.getAttribute('href') + ' ' + getComputedStyle(about).display : null, title:document.title, t:+b.t.toFixed(1) }; })()`;
const HAND = (type, u, v) => `(() => { const w = innerWidth, h = innerHeight, S = Math.min((w < 600 ? 0.94 : 0.80)*w/0.92, (w < 600 ? 0.62 : 0.74)*h/0.69);
  document.querySelector('canvas').dispatchEvent(new PointerEvent('${type}', { clientX:w/2 + (${u} - 0.5)*S, clientY:h/2 - (${v} - 0.5)*S, pointerId:1, pointerType:'mouse', bubbles:true })); })()`;
try {
  if (THIRST) {                                                     // the wall at five times of day, from the page itself
    await send('Runtime.enable'); await send('Log.enable'); await send('Page.enable');
    for (const d of [0.1, 0.3, 0.5, 0.7, 0.9]) {
      await send('Page.navigate', { url:url + (url.includes('?') ? '&' : '?') + 'solo&day=' + d }); errors.length = 0; let t = null;
      for (let i = 0; i < 30 && !t; i++) { await nap(500); t = await js(`window.__basin && __basin.thirst && __basin.thirst.cols ? JSON.stringify({ ...__basin.thirst, gl:document.querySelector('canvas').getContext('webgl2').getError() }) : null`).catch(() => null); }
      t = t && JSON.parse(t); console.log('day', d, JSON.stringify(t));
      need(t && t.wet >= 0.75, `day ${d}: wet ${t && t.wet}, under 0.75`); need(t && t.gl === 0, `day ${d}: GL error ${t && t.gl}`); need(errors.length === 0, `day ${d}: ${errors.slice(0, 2).join(' | ')}`); }
    console.log(fails.length ? 'FAIL: ' + fails.join('; ') : 'PASS: the about page\'s numbers are the thirst model\'s; the live page keeps 3/4 of the wall wet at days 0.1 to 0.9, GL error 0');
    ws.close(); process.exit(fails.length ? 1 : 0); }
  await send('Runtime.enable'); await send('Log.enable'); await send('Page.enable'); await send('Page.navigate', { url }); errors.length = 0;   // what the page before this one logged is not this page's
  const end = Date.now() + 45000; let s = null;                     // a sleeping spring is given up on after 20 s; then the reservoir pours
  while (Date.now() < end) { await nap(1000); s = await js(`window.__basin ? ${STATE} : null`).catch(() => null); if (s && s.water > 0.9) break; }
  if (!s) throw new Error('the page never set window.__basin: ' + url);
  console.log('pouring ', JSON.stringify(s));
  need(s.water > 0.9, `water ${s.water}, not above 0.9 within 45 s`); need(s.k === 0.25, `k is ${s.k}, not 0.25`);
  need(s.line === 'none', 'the line under the basin is showing'); need(s.rim !== null, 'no line on the drain\'s rim');
  need(s.about && s.about.startsWith('about.html') && !s.about.endsWith('none'), 'no about link');
  need(/^\[s\[i\|y\]n\[k\]\[w\]hole/.test(s.title), `title is "${s.title}"`);
  if (/spring=nofeed/.test(url)) need(s.res && s.res.on && s.res.runs > 0, 'no spring, and the reservoir is not pouring');
  const handIn = (held) => { console.log('hand in ', JSON.stringify(held)); need(held.grip > 0.3, `the drag did not grip (${held.grip})`); need(held.soft > 0.3, `the water did not go soft under the hand (${held.soft})`); };
  const handOut = (out) => { console.log('hand out', JSON.stringify(out));   // both modes: the hand's time told on the rim, in a clear breath
    need(/^lost = \d\d:\d\d$/.test(out.lost) && out.rim === out.lost, `the rim does not tell the hand's time ("${out.rim}")`); need(out.clear > 0.5, `no clear breath (${out.clear})`);
    need(out.rimOpacity > 0.4, `the rim's line is not showing in the clear breath (${out.rimOpacity})`); };
  const isGrid = await js('!!(window.__basin.hearts && window.__basin.hearts.grid)');
  if (isGrid) {   // ?r=grid, the default: the fall's flows, by real pointer events on the canvas
    const P = (t, x, y, id) => js(`document.querySelector('canvas').dispatchEvent(new PointerEvent('${t}', { clientX:${x}, clientY:${y}, pointerId:${id || 1}, pointerType:'mouse', isPrimary:true, bubbles:true, buttons:${t === 'pointerup' ? 0 : 1} })), 1`);
    const F = () => js('JSON.stringify(window.__basin.fall)').then(JSON.parse), W = await js('innerWidth'), H = await js('innerHeight'), cx = W/2, cy = H/2;
    const until = async (test, ms) => { const end = Date.now() + ms; let f = await F(); while (!test(f) && Date.now() < end) { await nap(100); f = await F(); } return f; };   // poll the page's own state, never its timings
    const expect = async (test, ms, what) => { const f = await until(test, ms); need(test(f), `${what} (${JSON.stringify(f)})`); return f; };   // poll, and fail out loud on a timeout
    const tap = async (x, y) => { await P('pointerdown', x, y); await P('pointerup', x, y); };
    const goIn = async () => { await expect((f) => f.z === 0 && f.in === null && f.f === null, 8000, 'never back on the wall'); await tap(0.3*W, 0.3*H); await expect((f) => f.f !== null, 2000, 'a tap on the wall did not start a fall into the copy (going in must be a fall, never a zoom)'); return expect((f) => f.in !== null && f.z === 1 && f.f === null, 8000, 'a tap on the wall did not fall into the copy and arrive'); };   // going in and out are falls through the drain: wait for each to end
    const drag = async (x0, y0, x1, y1) => { await P('pointerdown', x0, y0); for (let i = 1; i <= 15; i++) { await P('pointermove', x0 + (x1 - x0)*i/15, y0 + (y1 - y0)*i/15); await nap(40); } };
    let f = await goIn();
    await tap(cx, cy); await expect((f) => f.f !== null, 2000, 'a tap on the drain did not start a fall');
    await expect((f) => f.f === null && f.depth === 1 && f.in !== null, 20000, 'the fall did not come back to the same basin, one ring deeper');
    await drag(cx, cy, cx, cy + 0.2*H); await expect((f) => f.climb > 0.1, 3000, 'a pull from the drain did not grip');
    await P('pointerup', cx, cy + 0.2*H); await expect((f) => f.in !== null && f.climb === 0, 5000, 'a short pull did not slide back in');
    await drag(cx, cy, cx, H - 2); await expect((f) => f.in === null, 6000, 'a pull to the rim did not climb out'); await P('pointerup', cx, H - 2);
    await goIn(); await drag(0.25*W, 0.3*H, 0.2*W, 0.25*H); await nap(1200); handIn(await js(STATE)); f = await F(); await P('pointerup', 0.2*W, 0.25*H);
    need(f.in !== null, `a hold away from the drain did not stay in (${JSON.stringify(f)})`); await nap(1500); handOut(await js(STATE));
    await js('window.__basin.idle(30.1), 1'); await expect((f) => f.f !== null, 2000, 'past 30 s alone, no fall out began'); await expect((f) => f.in === null, 6000, 'past 30 s alone, the fall did not come out on the wall');
    await goIn(); await P('pointerdown', 0.2*W, 0.2*H, 1); await P('pointerdown', 0.8*W, 0.8*H, 2); await P('pointerup', 0.2*W, 0.2*H, 1); await P('pointerup', 0.8*W, 0.8*H, 2);
    await expect((f) => f.f !== null, 2000, 'two fingers did not start a fall out'); await expect((f) => f.in === null, 6000, 'two fingers did not go out');
    // the hearts: 30 minutes run ahead (__basin.beats). Neighbours must fall into step and slip out of it, and every heart must keep beating at about its own pace
    // no borders: every dot of the wall's lattice drawn by exactly one copy. One probe frame, each kept dot half grey and the copies added: 128 everywhere, never 0 (a gap) or 255 (drawn twice)
    const own = await js('__basin.own()');
    need(own.corner, 'the probe frame on the wall was drawn without the corner\'s lens');   // the wall is always seen through the corner's mass: the proof must be too
    await send('Emulation.setDeviceMetricsOverride', { width:960, height:721, deviceScaleFactor:1, mobile:false }); await nap(900);   // an odd height: a cell edge on a row of pixel centres, where one row was once drawn twice or not at all
    const odd = await js('__basin.own()'); await send('Emulation.clearDeviceMetricsOverride'); await nap(900);
    need(odd.gaps === 0 && odd.twice === 0 && own.gaps === 0 && own.twice === 0, `a row of the wall is drawn by no copy or by two: at an odd height ${odd.gaps} gaps, ${odd.twice} twice, in ${JSON.stringify(odd.box)}`);
    need(own.lo >= 126 && own.hi <= 130, `on the wall a dot is drawn ${own.lo < 126 ? 'by no copy' : 'by two copies'}: probe pixels run ${own.lo} to ${own.hi}, not 128`);
    await js('__basin.tap(innerWidth*0.3, innerHeight*0.3)'); const mid = await js('__basin.own(true)');   // going in, the copy you enter takes dots over: still never two copies on one dot (the drain's lens may leave gaps)
    need(mid.twice <= 16, `on the way into a copy ${mid.twice} pixels are drawn by two copies at ${mid.kin} of the way (up to 16 of ${mid.of} are let pass: through the lens the bent lattice can land on a pixel's centre, and rounding gives that pixel to both)`);
    console.log('borders ', JSON.stringify({ wall:own, goingIn:mid }));
    // the hearts: 30 minutes run ahead (__basin.beats; it moves the page's clock, so it stays last). Neighbours must fall into step and then slip out of it again, and every heart must keep beating
    const STALL = 1200;                                              // beats in 30 minutes below which a heart has stalled: 0.67 a second, where the slowest rests at 0.87
    const hs = await js(`(() => { const g = __basin.hearts.grid, n0 = g.hearts.map((h) => h.nb), s = __basin.beats(1800), nb = g.hearts.map((h, i) => h.nb - n0[i]), up = s.findIndex((v) => v > 0.55);
      let lockings = 0, on = false; for (const v of s) { if (!on && v > 0.55) { on = true; lockings++; } else if (on && v < 0.3) on = false; }
      return { lo:Math.min(...s), hi:Math.max(...s), slipsAfterLock:up >= 0 && s.slice(up).some((v) => v < 0.3), lockings, least:Math.min(...nb), most:Math.max(...nb), alive:__basin.thirst.beating }; })()`);
    console.log('hearts  ', JSON.stringify(hs));
    need(hs.alive === 48 && hs.least > STALL, `a heart stopped or stalled in 30 minutes: ${hs.alive} of 48 beating, the slowest ${hs.least} beats`);
    need(hs.hi > 0.55, `the hearts never fall into step: the share of neighbours in step never passes ${hs.hi}`);
    need(hs.slipsAfterLock && hs.lockings >= 2, `the hearts lock and never slip: after first falling into step the share never drops under 0.3 and rises again (${hs.lockings} lockings)`);
  } else {                                                         // one basin: a hand in the water, then the rim tells its time
    await js(HAND('pointermove', 0.62, 0.60)); await js(HAND('pointerdown', 0.62, 0.60));
    for (let i = 1; i <= 30; i++) { await js(HAND('pointermove', 0.62 - 0.004*i, 0.60 - 0.002*i)); await nap(33); }
    handIn(await js(STATE));
    await nap(1200); await js(HAND('pointerup', 0.50, 0.54)); await nap(1500);
    handOut(await js(STATE));
  }
  // the way to the about page, last (it leaves the page): by a key on both addresses; on the wall through the heavy corner, by a key and by a tap
  const there = async (what) => { const end = Date.now() + 12000; let at = ''; while (Date.now() < end && !/about\.html$/.test(at)) { await nap(150); at = await js('location.pathname').catch(() => ''); }
    need(/about\.html$/.test(at), `${what} did not reach about.html (at ${at})`); await nap(400); need(/hole/.test(await js('document.title').catch(() => '')), `${what}: the about page did not load`); };
  const enter = async () => { need(await js(`(() => { const a = document.getElementById('about'); a.focus(); return document.activeElement === a && getComputedStyle(a).display !== 'none' && getComputedStyle(a).visibility !== 'hidden'; })()`), 'the about link does not take focus');
    for (const type of ['keyDown', 'keyUp']) await send('Input.dispatchKeyEvent', { type, key:'Enter', code:'Enter', windowsVirtualKeyCode:13, nativeVirtualKeyCode:13, ...(type === 'keyDown' ? { text:'\r' } : {}) }); };
  if (isGrid) {
    const wall = async () => { await send('Page.navigate', { url }); let c = null; for (let i = 0; i < 100 && !(c && c.on === 1 && c.p === null); i++) { await nap(200); c = await js('window.__basin && __basin.fall.z === 0 && __basin.fall.f === null ? __basin.corner : null').catch(() => null); } return c; };
    const falling = async (what) => { let c = null; for (let i = 0; i < 20 && !(c && c.p > 0); i++) { await nap(100); c = await js('window.__basin ? __basin.corner : null').catch(() => null); if (!c) break; }   // no __basin: already through
      need(!c || c.p > 0, `${what} did not start the fall into the corner (${JSON.stringify(c)})`); };
    let c = await wall(); console.log('corner  ', JSON.stringify(c));
    need(c && c.re > 0 && c.on === 1, `on the wall the corner's mass is not there at rest (${JSON.stringify(c)})`);
    await enter(); await falling('Enter on the about link'); await there('Enter on the about link');
    await wall(); const W = await js('innerWidth'), H = await js('innerHeight');
    const cornerTap = async () => { for (const t of ['pointerdown', 'pointerup']) await js(`document.querySelector('canvas').dispatchEvent(new PointerEvent('${t}', { clientX:${W - 14}, clientY:${H - 14}, pointerId:1, pointerType:'mouse', isPrimary:true, bubbles:true, buttons:${t === 'pointerup' ? 0 : 1} })), 1`); };
    const settle = async (what) => { let c = null; for (let i = 0; i < 80 && !(c && c.p === null); i++) { await nap(100); c = await js('window.__basin ? __basin.corner : null').catch(() => null); }   // a fall turned round, or the way back: the corner lets go and the wall is as it was
      need(c && c.p === null && /\/$|index\.html$/.test(await js('location.pathname')), `${what}: the corner did not let go on the wall (${JSON.stringify(c)})`); };
    await cornerTap(); await falling('a tap in the bottom right corner'); await nap(500);   // Escape part of the way down: back out, and still on this page
    await js(`dispatchEvent(new KeyboardEvent('keydown', { key:'Escape', bubbles:true })), 1`);   // made in the page, as the taps are: a real Escape through the debugger hides a headless tab, and a hidden tab draws no frames
    await settle('Escape during the fall into the corner');
    await cornerTap(); await falling('a tap in the bottom right corner'); await there('a tap in the bottom right corner');
    // the way back: the about page's own link (pointed at this build, where it names the live one), the dark closing over the page, and the wall opening out of its corner
    let home = false; for (let i = 0; i < 40 && !home; i++) { await js('scrollTo(0, document.documentElement.scrollHeight), 1'); await nap(150); home = await js(`!!document.querySelector('a[data-piece="home"]')`); }   // the page furnishes itself on a scroll: its links are there after one
    need(home, 'the about page has no way back to the piece');
    if (home) await js(`document.querySelectorAll('a[data-piece="home"]').forEach((a) => { a.href = ${JSON.stringify(url)}; }), document.querySelector('a[data-piece="home"]').click(), 1`);
    let back = null; for (let i = 0; i < 80 && !(back && back.p > 0); i++) { await nap(100); back = await js('window.__basin ? __basin.corner : null').catch(() => null); }
    need(back && back.p > 0.3, `back from the about page the wall did not open out of the corner (${JSON.stringify(back)})`);
    await settle('the way back from the about page');
  } else { await enter(); await there('Enter on the about link'); }
  if (png) { const { data } = await send('Page.captureScreenshot', { format:'png' }); fs.writeFileSync(png, Buffer.from(data, 'base64')); console.log('wrote', png); }
  const bad = errors.filter((e) => !/\/nofeed\//.test(e) && !/\/feed\/now\.json/.test(e));   // and the about page's live frame asks the real spring, which may be down: not this build's error          // ?spring=nofeed/ is a spring that is not there on purpose: its 404 is the test, not an error
  need(bad.length === 0, `${bad.length} errors logged: ${bad.slice(0, 3).join(' | ')}`);
  console.log(fails.length ? 'FAIL: ' + fails.join('; ') : isGrid ? 'PASS: water, the grid: in, through, back, a hold, out, alone, two fingers; every dot drawn once; hearts in and out of step; the corner and the about link both reach the about page, Escape backs out of the corner, and the way back opens out of it; no errors' : 'PASS: water, the default look, the hand, the rim, the about link by a key, no errors');
} finally { ws.close(); }
process.exit(fails.length ? 1 : 0);
