#!/usr/bin/env node
// One real-time check of [syn[k]]hole, dry season, on any address (a local port, or the public one after a publish). Node 22+, no packages.
// It loads the page in a headless Chrome, lets it pour, puts a hand in, drags, lets go, and fails (exit 1) unless:
//   the water runs, the look is the default (k 0.25, no line under the basin, the code on the drain's rim), the reservoir pours when no
//   spring answers, the drag grips, the hand's time is told on the way out, and the page logged no error.
//   1. a headless Chrome:  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --remote-debugging-port=9396 \
//        --user-data-dir=<a temp folder> --window-size=960,720 --hide-scrollbars --enable-gpu --use-angle=metal --ignore-gpu-blocklist about:blank
//   2. node src/check.mjs http://127.0.0.1:8806/            the spring's water if it is awake, else the reservoir
//      node src/check.mjs "http://127.0.0.1:8806/?spring=nofeed/"     no spring: the reservoir must pour
//   CHECK_PORT=<port> picks another Chrome; a second argument writes a PNG of the page after the hand has left.
//   node src/check.mjs --thirst [address of synkhole/]     the thirst schedule instead (index.html dryOf). With no browser: about.html carries index.html's
//      dawnDay, dryOf and tilt lines character for character, and every clock time and count the about page quotes is solved again from dryOf over the
//      48 ranks k/47. With an address and the Chrome: days 0.1, 0.3, 0.5, 0.7, 0.9 each leave at least 3/4 of the wall wet (__basin.thirst.wet), GL error 0.
import fs from 'node:fs';
const ARGS = process.argv.slice(2), THIRST = ARGS.includes('--thirst'), [url, png] = ARGS.filter((a) => a !== '--thirst');
const PORT = +process.env.CHECK_PORT || 9396, nap = (ms) => new Promise((r) => setTimeout(r, ms));
if (!url && !THIRST) { console.log('usage: node src/check.mjs <address> [out.png]   or   node src/check.mjs --thirst [address]'); process.exit(2); }
const fails = [], need = (ok, what) => { if (!ok) fails.push(what); };
if (THIRST) {                                                       // the page's numbers, from the code that makes them
  const read = (f) => fs.readFileSync(new URL(f, import.meta.url), 'utf8'), idx = read('index.html'), abt = read('about.html');
  const line = (text, name) => (text.match(new RegExp(`^const ${name} = .*$`, 'm')) || [''])[0];
  for (const n of ['dawnDay', 'dryOf', 'tilt']) { const a = line(idx, n); need(a, `index.html has no line "const ${n} = ..."`); need(!a || a === line(abt, n), `about.html's ${n} is not index.html's, character for character`); }
  const KSS = '(a, b, x) => { const t = Math.max(0, Math.min(1, (x - a)/(b - a))); return t*t*(3 - 2*t); }', kss = eval(KSS);
  need(idx.includes('const kss = ' + KSS), 'index.html\'s kss is not the smoothstep this check solves with');
  const dryOf = new Function('kss', line(idx, 'dryOf').replace(/^const dryOf = /, 'return ').replace(/;\s+\/\/.*$/, ';'))(kss);
  const R = [...Array(48)].map((_, k) => k/47), n = (p, cut) => R.filter((r) => dryOf(r, p) > cut).length, S = 1/86400;   // a second of the day; p 0 is 6 am
  const clock = (p) => { const m = Math.floor(360 + p*1440 + 1e-9) % 1440, h = Math.floor(m/60); return `${(h + 11) % 12 + 1}:${String(m % 60).padStart(2, '0')} ${h < 12 ? 'am' : 'pm'}`; };
  let first = null, last = null, most = 0, untouched = 48; const hrs = R.map(() => 0);
  for (let k = 0; k < 86400; k++) { const p = k*S, any = n(p, 0); if (any && first === null) first = p; if (any) last = p;
    most = Math.max(most, n(p, 0.5)); untouched = Math.min(untouched, 48 - any); R.forEach((r, i) => { if (dryOf(r, p) > 0.5) hrs[i] += 24*S; }); }
  const WORD = ['zero', 'one', 'two', 'three', 'four', 'five', 'six'], lo = Math.round(Math.min(...hrs)), hi = Math.round(Math.max(...hrs));
  const want = [`from ${clock(first)} the dry passes over it`, `by ${clock(last + S)} every copy is full again`, `for about ${WORD[lo]} to ${WORD[hi]} hours`,
    `counting a copy dry once half its ink is gone, ${n(0.25, 0.5)} are dry at noon, ${n(0.5, 0.5)} at 6 pm, never more than ${most}`, `at least ${untouched} of the 48 untouched at any hour`];
  console.log('solved  ', JSON.stringify({ first:clock(first), full:clock(last + S), hours:[+Math.min(...hrs).toFixed(2), +Math.max(...hrs).toFixed(2)], noon:n(0.25, 0.5), six:n(0.5, 0.5), most, untouched }));
  for (const w of want) need(abt.includes(w), `about.html does not say "${w}"`);
  if (!url) { console.log(fails.length ? 'FAIL: ' + fails.join('; ') : 'PASS: about.html matches dryOf, dawnDay and tilt, and its clock times and counts'); process.exit(fails.length ? 1 : 0); }
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
    console.log(fails.length ? 'FAIL: ' + fails.join('; ') : 'PASS: about.html matches dryOf, dawnDay and tilt and its numbers; 3/4 of the wall wet at days 0.1 to 0.9');
    ws.close(); process.exit(fails.length ? 1 : 0); }
  await send('Runtime.enable'); await send('Log.enable'); await send('Page.enable'); await send('Page.navigate', { url }); errors.length = 0;   // what the page before this one logged is not this page's
  const end = Date.now() + 45000; let s = null;                     // a sleeping spring is given up on after 20 s; then the reservoir pours
  while (Date.now() < end) { await nap(1000); s = await js(`window.__basin ? ${STATE} : null`).catch(() => null); if (s && s.water > 0.9) break; }
  if (!s) throw new Error('the page never set window.__basin: ' + url);
  console.log('pouring ', JSON.stringify(s));
  need(s.water > 0.9, `water ${s.water}, not above 0.9 within 45 s`); need(s.k === 0.25, `k is ${s.k}, not 0.25`);
  need(s.line === 'none', 'the line under the basin is showing'); need(s.rim !== null, 'no line on the drain\'s rim');
  need(s.about && s.about.startsWith('about.html') && !s.about.endsWith('none'), 'no about link');
  need(/^\[syn\[k\]\]hole/.test(s.title), `title is "${s.title}"`);
  if (/spring=nofeed/.test(url)) need(s.res && s.res.on && s.res.runs > 0, 'no spring, and the reservoir is not pouring');
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
