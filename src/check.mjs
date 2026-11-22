#!/usr/bin/env node
// One real-time check of [syn[k]]hole, dry season, on any address (a local port, or the public one after a publish). Node 22+, no packages.
// It loads the page in a headless Chrome, lets it pour, puts a hand in, drags, lets go, and fails (exit 1) unless:
//   the water runs, the look is the default (k 0.25, no line under the basin, the code on the drain's rim), the reservoir pours when no
//   spring answers, the drag grips, the hand's time is told on the way out, and the page logged no error.
//   On the grid (?r=grid, the bare address) it checks the fall instead: a tap goes in, a drain tap falls through to depth 1, a short pull
//   slides back, a pull to the rim climbs out, 30 s alone floats up, two fingers go out.
//   1. a headless Chrome:  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --remote-debugging-port=9396 \
//        --user-data-dir=<a temp folder> --window-size=960,720 --hide-scrollbars --enable-gpu --use-angle=metal --ignore-gpu-blocklist about:blank
//   2. node src/check.mjs http://127.0.0.1:8806/            the spring's water if it is awake, else the reservoir
//      node src/check.mjs "http://127.0.0.1:8806/?spring=nofeed/"     no spring: the reservoir must pour
//   CHECK_PORT=<port> picks another Chrome; a second argument writes a PNG of the page after the hand has left.
import fs from 'node:fs';
const PORT = +process.env.CHECK_PORT || 9396, [url, png] = process.argv.slice(2), nap = (ms) => new Promise((r) => setTimeout(r, ms));
if (!url) { console.log('usage: node src/check.mjs <address> [out.png]'); process.exit(2); }
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
const STATE = `(() => { const b = window.__basin, q = b.kq, code = document.getElementById('code'), rim = document.querySelector('svg text'), about = document.getElementById('about');
  return { water:+b.water.toFixed(3), k:b.k, grip:+b.grip.toFixed(3), soft:+q.soft.toFixed(2), clear:+q.clear.toFixed(2), lost:q.lost, clock:+q.w.toFixed(2), seq:b.seq, prompt:b.prompt.slice(0, 40),
    res:b.res, line:getComputedStyle(code).display, rim:rim ? rim.textContent : null, rimOpacity:rim ? +rim.ownerSVGElement.style.opacity : null,
    about:about ? about.getAttribute('href') + ' ' + getComputedStyle(about).display : null, title:document.title, t:+b.t.toFixed(1) }; })()`;
const HAND = (type, u, v) => `(() => { const w = innerWidth, h = innerHeight, S = Math.min((w < 600 ? 0.94 : 0.80)*w/0.92, (w < 600 ? 0.62 : 0.74)*h/0.69);
  document.querySelector('canvas').dispatchEvent(new PointerEvent('${type}', { clientX:w/2 + (${u} - 0.5)*S, clientY:h/2 - (${v} - 0.5)*S, pointerId:1, pointerType:'mouse', bubbles:true })); })()`;
const fails = [], need = (ok, what) => { if (!ok) fails.push(what); };
try {
  await send('Runtime.enable'); await send('Log.enable'); await send('Page.enable'); await send('Page.navigate', { url }); errors.length = 0;   // what the page before this one logged is not this page's
  const end = Date.now() + 45000; let s = null;                     // a sleeping spring is given up on after 20 s; then the reservoir pours
  while (Date.now() < end) { await nap(1000); s = await js(`window.__basin ? ${STATE} : null`).catch(() => null); if (s && s.water > 0.9) break; }
  if (!s) throw new Error('the page never set window.__basin: ' + url);
  console.log('pouring ', JSON.stringify(s));
  need(s.water > 0.9, `water ${s.water}, not above 0.9 within 45 s`); need(s.k === 0.25, `k is ${s.k}, not 0.25`);
  need(s.line === 'none', 'the line under the basin is showing'); need(s.rim !== null, 'no line on the drain\'s rim');
  need(s.about && s.about.startsWith('about.html') && !s.about.endsWith('none'), 'no about link');
  need(/^\[s\[i\/y\]n\[k\]\[w\]hole/.test(s.title), `title is "${s.title}"`);
  if (/spring=nofeed/.test(url)) need(s.res && s.res.on && s.res.runs > 0, 'no spring, and the reservoir is not pouring');
  if (await js('!!(window.__basin.hearts && window.__basin.hearts.grid)')) {   // ?r=grid, the default: the fall's flows, by real pointer events on the canvas
    const P = (t, x, y, id) => js(`document.querySelector('canvas').dispatchEvent(new PointerEvent('${t}', { clientX:${x}, clientY:${y}, pointerId:${id || 1}, pointerType:'mouse', isPrimary:true, bubbles:true, buttons:${t === 'pointerup' ? 0 : 1} })), 1`);
    const F = () => js('JSON.stringify(window.__basin.fall)').then(JSON.parse), W = await js('innerWidth'), H = await js('innerHeight'), cx = W/2, cy = H/2;
    const tap = async (x, y) => { await P('pointerdown', x, y); await P('pointerup', x, y); };
    const pull = async (to) => { await P('pointerdown', cx, cy); for (let i = 1; i <= 15; i++) { await P('pointermove', cx, cy + (to - cy)*i/15); await nap(40); } await P('pointerup', cx, to); };
    await tap(0.3*W, 0.3*H); await nap(1500); let f = await F(); need(f.in !== null, `a tap on the wall did not go in (${JSON.stringify(f)})`);
    await tap(cx, cy); await nap(4300); f = await F(); need(f.f === null && f.depth === 1, `a tap on the drain did not fall through to depth 1 (${JSON.stringify(f)})`);
    await pull(cy + 0.2*H); await nap(1200); f = await F(); need(f.in !== null && f.climb < 0.05, `a short pull did not slide back in (${JSON.stringify(f)})`);
    await pull(H - 2); await nap(300); f = await F(); need(f.in === null, `a pull to the rim did not climb out (${JSON.stringify(f)})`);
    await nap(1500); await tap(0.3*W, 0.3*H); await nap(1500); await js('window.__basin.hearts.grid.idle = 29.9, 1'); await nap(500); f = await F(); need(f.in === null, `30 s alone did not float up (${JSON.stringify(f)})`);
    await nap(3000); await tap(0.3*W, 0.3*H); await nap(1500); await P('pointerdown', 0.2*W, 0.2*H, 1); await P('pointerdown', 0.8*W, 0.8*H, 2); await P('pointerup', 0.2*W, 0.2*H, 1); await P('pointerup', 0.8*W, 0.8*H, 2);
    await nap(300); f = await F(); need(f.in === null, `two fingers did not go out (${JSON.stringify(f)})`);
    const bad = errors.filter((e) => !/\/nofeed\//.test(e)); need(bad.length === 0, `${bad.length} errors logged: ${bad.slice(0, 3).join(' | ')}`);
    console.log(fails.length ? 'FAIL: ' + fails.join('; ') : 'PASS: the grid, in, through, back, out, alone, two fingers, no errors');
    process.exit(fails.length ? 1 : 0);
  }
  await js(HAND('pointermove', 0.62, 0.60)); await js(HAND('pointerdown', 0.62, 0.60));
  for (let i = 1; i <= 30; i++) { await js(HAND('pointermove', 0.62 - 0.004*i, 0.60 - 0.002*i)); await nap(33); }
  const held = await js(STATE); console.log('hand in ', JSON.stringify(held));
  need(held.grip > 0.3, `the drag did not grip (${held.grip})`); need(held.soft > 0.3, `the water did not go soft under the hand (${held.soft})`);
  await nap(1200); await js(HAND('pointerup', 0.50, 0.54)); await nap(1500);
  const out = await js(STATE); console.log('hand out', JSON.stringify(out));
  need(/^lost = \d\d:\d\d$/.test(out.lost) && out.rim === out.lost, `the rim does not tell the hand's time ("${out.rim}")`); need(out.clear > 0.5, `no clear breath (${out.clear})`);
  need(out.rimOpacity > 0.4, `the rim's line is not showing in the clear breath (${out.rimOpacity})`);
  if (png) { const { data } = await send('Page.captureScreenshot', { format:'png' }); fs.writeFileSync(png, Buffer.from(data, 'base64')); console.log('wrote', png); }
  const bad = errors.filter((e) => !/\/nofeed\//.test(e));          // ?spring=nofeed/ is a spring that is not there on purpose: its 404 is the test, not an error
  need(bad.length === 0, `${bad.length} errors logged: ${bad.slice(0, 3).join(' | ')}`);
  console.log(fails.length ? 'FAIL: ' + fails.join('; ') : 'PASS: water, the default look, the hand, the rim, no errors');
} finally { ws.close(); }
process.exit(fails.length ? 1 : 0);
