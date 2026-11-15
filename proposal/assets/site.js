/* ===== Inovosense · از عمق تا نور · v2 ===== */
/* Media swap: put the finished reels in media/ and write their file names here. */
const MEDIA = {
  reel1: '',   // «لبخندمو دوست دارم»   e.g. 'media/reel-labkhand.mp4'
  reel2: '',   // «از قنات تا پوست»     e.g. 'media/reel-qanat.mp4'
  reel3: ''    // «جعبه رو برگردون»     e.g. 'media/reel-jabe.mp4'
};

const FA = s => String(s).replace(/\d/g, d => '۰۱۲۳۴۵۶۷۸۹'[d]);
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const POSTS = window.IG_POSTS || {};
const EXT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>';

/* one-shot triggers (content is always visible; these only start animations) */
const io = new IntersectionObserver(es => es.forEach(e => {
  if (!e.isIntersecting) return;
  const el = e.target; el.classList.add('in'); io.unobserve(el);
  if (el.dataset.count) count(el);
  if (el.id === 'bigq') typeQ(el);
  if (el.classList.contains('dm-b')) el.parentElement.classList.add('dm-in');
}), { threshold: .2 });
$$('[data-count],#bigq,.tl,.bud,.dm-b,.chap').forEach(el => io.observe(el));

function count(el) {
  const to = +el.dataset.count, t0 = performance.now();
  if (reduce) { el.textContent = FA(to); return; }
  const step = t => { const k = Math.min(1, (t - t0) / 1600); el.textContent = FA(Math.round(to * (1 - Math.pow(1 - k, 3)))); if (k < 1) requestAnimationFrame(step); };
  requestAnimationFrame(step);
}
function typeQ(el) {
  const span = $('.typed', el), full = span.dataset.t; let i = 0;
  if (reduce) { el.classList.add('done'); return; }
  span.textContent = '';
  const tick = () => { span.textContent = full.slice(0, ++i); if (i < full.length) setTimeout(tick, 55 + Math.random() * 45); else el.classList.add('done'); };
  setTimeout(tick, 300);
}

/* nav colour follows the zone under it; the depth gauge follows the page */
const nav = $('.nav'), gb = $('.gauge b'), links = $$('.nav ul a');
const secs = links.map(a => $(a.getAttribute('href'))).filter(Boolean);
function onScroll() {
  const y = scrollY, h = document.documentElement.scrollHeight - innerHeight;
  nav.classList.toggle('solid', y > innerHeight * .6);
  nav.style.pointerEvents = 'none';
  const under = document.elementFromPoint(innerWidth / 2, 70);
  nav.style.pointerEvents = '';
  const zone = under && under.closest('.z-d,.z-m,.z-l');
  nav.classList.toggle('on-l', !!zone && zone.classList.contains('z-l'));
  if (gb) gb.style.bottom = `calc(${(y / h) * 100}% - 6px)`;
  let cur = null; secs.forEach(s => { if (s.getBoundingClientRect().top < innerHeight * .4) cur = s; });
  links.forEach(a => a.classList.toggle('on', !!cur && a.getAttribute('href') === '#' + cur.id));
}
addEventListener('scroll', onScroll, { passive: true }); onScroll();

/* ===== Instagram phones ===== */
function wirePhone(ph) {
  const view = $('.ig-post', ph); if (!view) return null;
  const track = $('.track', view), dots = $('.dots', view), cnt = $('.cnt', view), cap = $('.cap', view), heart = $('.heart', view), lk = $('.lkb', view);
  const car = $('.car', view);
  car.insertAdjacentHTML('beforeend', '<button class="nav-a prev" aria-label="اسلاید قبلی"></button><button class="nav-a next" aria-label="اسلاید بعدی"></button>');
  const prev = $('.nav-a.prev', car), next = $('.nav-a.next', car);
  const idx = () => Math.round(track.scrollLeft / track.clientWidth);
  const goTo = i => { const n = track.children.length; i = Math.max(0, Math.min(n - 1, i)); track.scrollTo({ left: i * track.clientWidth, behavior: 'smooth' }); };
  const arrows = () => { const n = track.children.length, i = idx(); prev.hidden = n < 2 || i === 0; next.hidden = n < 2 || i >= n - 1; };
  prev.addEventListener('click', e => { e.stopPropagation(); goTo(idx() - 1); });
  next.addEventListener('click', e => { e.stopPropagation(); goTo(idx() + 1); });
  dots.addEventListener('click', e => { const d = e.target.closest('i'); if (d) goTo([...dots.children].indexOf(d)); });
  function open(id) {
    const p = POSTS[id]; if (!p) return;
    track.innerHTML = p.imgs.map(s => `<img src="${s}" alt="" draggable="false">`).join('');
    track.scrollLeft = 0;
    const n = p.imgs.length;
    dots.innerHTML = n > 1 ? p.imgs.map((_, i) => `<i class="${i ? '' : 'on'}"></i>`).join('') : '';
    cnt.style.display = n > 1 ? '' : 'none'; cnt.textContent = FA(`1/${n}`); cnt.dir = 'ltr';
    const h = p.h || $('.ig-top .u', ph).textContent;
    cap.innerHTML = `<b>${h}</b>${p.cap}` + (p.url ? `<br><a href="${p.url}" target="_blank" rel="noopener">${EXT}${p.ul || 'دیدن در اینستاگرام'}</a>` : `<span class="t">نمونهٔ پیشنهادی</span>`);
    lk.classList.remove('on'); view.classList.add('open'); view.scrollTop = 0; arrows();
  }
  ph.addEventListener('click', e => { const b = e.target.closest('.ig-grid button[data-p]'); if (b) open(b.dataset.p); });
  $('.back', view).addEventListener('click', () => view.classList.remove('open'));
  track.addEventListener('scroll', () => {
    const n = track.children.length; arrows(); if (n < 2) return;
    const i = Math.round(track.scrollLeft / track.clientWidth);
    $$('i', dots).forEach((d, k) => d.classList.toggle('on', k === i)); cnt.textContent = FA(`${i + 1}/${n}`);
  }, { passive: true });
  let last = 0;
  track.addEventListener('pointerup', () => { const t = Date.now(); if (t - last < 320) { heart.classList.remove('pop'); void heart.offsetWidth; heart.classList.add('pop'); lk.classList.add('on'); } last = t; });
  lk.addEventListener('click', () => lk.classList.toggle('on'));
  let d = false, x0 = 0, s0 = 0;
  track.addEventListener('pointerdown', e => { if (e.pointerType !== 'mouse') return; d = true; x0 = e.clientX; s0 = track.scrollLeft; track.style.scrollSnapType = 'none'; });
  addEventListener('pointermove', e => { if (d) track.scrollLeft = s0 - (e.clientX - x0); });
  addEventListener('pointerup', () => { if (!d) return; d = false; track.style.scrollSnapType = ''; const w = track.clientWidth; track.scrollTo({ left: Math.round(track.scrollLeft / w) * w, behavior: 'smooth' }); });
  return { open, close: () => view.classList.remove('open'), view, track };
}
const phones = {};
$$('.phone').forEach(ph => { if (ph.id) phones[ph.id] = wirePhone(ph); });

/* the proposed page opens its carousel once, as a hint */
const pn = phones['ph-new'];
if (pn && !reduce) {
  new IntersectionObserver((es, o) => { if (!es[0].isIntersecting) return; o.disconnect();
    setTimeout(() => pn.open('f1'), 1200);
    setTimeout(() => pn.track.scrollTo({ left: pn.track.clientWidth, behavior: 'smooth' }), 2700);
    setTimeout(() => pn.close(), 6200);
  }, { threshold: .6 }).observe($('#ph-new'));
}

/* ===== reference browser ===== */
const BR = window.BRANDS || [];
const refPh = $('#ph-ref'), note = $('.bnote'), go = $('.golink');
function showBrand(i) {
  const b = BR[i]; if (!b || !refPh) return;
  $$('.blist button').forEach((x, k) => { x.classList.toggle('on', k === i); x.setAttribute('aria-selected', k === i); });
  phones['ph-ref'] && phones['ph-ref'].close();
  $('.ig-top .u', refPh).textContent = b.h || b.n;
  $('.ig-av span', refPh).innerHTML = `<b>${b.n[0]}</b>`;
  $('.ig-post .ph .av', refPh).innerHTML = `<b>${b.n[0]}</b>`;
  $('.ig-post .ph .u', refPh).textContent = b.h || b.n;
  $('.ig-st', refPh).innerHTML = b.f ? `<div><b>${b.f}</b><span>دنبال‌کننده</span></div>` : '';
  $('.ig-bio', refPh).innerHTML = `<b>${b.n}</b><em>${b.tag}</em>` + (b.h ? `<span class="lk">instagram.com/${b.h}</span>` : '');
  const RM = '<svg class="ml" viewBox="0 0 24 24" fill="#fff"><path d="M4 3h16a1 1 0 0 1 1 1v16a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1Zm6 6v7l6-3.5L10 9Z"/></svg>';
  $('.ig-grid', refPh).innerHTML = b.tiles.length
    ? b.tiles.map(t => t.img
        ? `<button data-p="${t.key}" aria-label="باز کردن پست"><img src="${t.img}" alt="">${t.kind === 'reel' ? RM : ''}</button>`
        : `<a class="xl" href="${t.href}" target="_blank" rel="noopener" aria-label="دیدن این پست در اینستاگرام">${EXT}<span>دیدن در اینستاگرام</span></a>`).join('')
    : `<div class="ig-empty">این برند پیج فعالی ندارد.</div>`;
  let hlb = $('.ig-hl', refPh);
  if (!hlb) { hlb = document.createElement('div'); hlb.className = 'ig-hl'; $('.ig-tabs', refPh).before(hlb); }
  hlb.innerHTML = (b.hl || []).map(t => `<div><i><span></span></i>${t}</div>`).join('');
  hlb.hidden = !(b.hl && b.hl.length);
  const wc = $('.webcard', note);
  if (wc) {
    wc.href = b.w; $('em', wc).textContent = b.w.replace('https://', '');
    const im = $('img', wc);
    if (b.web) { im.src = b.web; im.hidden = false; wc.classList.remove('noimg'); } else { im.hidden = true; wc.classList.add('noimg'); }
  }
  $('.ig', refPh).scrollTop = 0;
  if (b.url) { go.href = b.url; go.classList.remove('off'); } else go.classList.add('off');
  note.classList.remove('swap'); void note.offsetWidth; note.classList.add('swap');
  $('.btag', note).textContent = b.tag; $('.bname', note).textContent = b.n;
  ['why', 'idea', 'les', 'use'].forEach(k => { const dd = $(`[data-k="${k}"]`, note); dd.textContent = b[k] || ''; dd.parentElement.hidden = !b[k]; });
}
$$('.blist button').forEach((x, i) => x.addEventListener('click', () => showBrand(i)));
if (BR.length) showBrand(0);

/* before / after */
$$('.ba-frame').forEach(f => { const r = $('input', f); const set = () => f.style.setProperty('--p', r.value + '%'); r.addEventListener('input', set); set(); });

/* the card */
const lc = $('.lcard');
if (lc) {
  const cue = $('.opencue');
  const t = () => { lc.classList.toggle('open'); cue.textContent = lc.classList.contains('open') ? 'بستن کارت' : 'باز کردن کارت'; };
  lc.addEventListener('click', t); cue.addEventListener('click', t);
}

/* card: two sample states */
$$('.cstates button').forEach(b => b.addEventListener('click', () => {
  $$('.cstates button').forEach(x => x.classList.toggle('on', x === b));
  const c = $('.lcard'); c.classList.toggle('st-b', b.dataset.s === 'b'); if (!c.classList.contains('open')) c.click();
}));

/* donut ↔ list */
const donut = $('.donut');
if (donut) {
  const segs = $$('circle.s', donut), rows = $$('.slist li'), mb = $('.mid b', donut), ms = $('.mid span', donut);
  const def = [mb.textContent, ms.textContent];
  const on = i => { donut.classList.add('dim'); segs.forEach((s, k) => s.classList.toggle('on', k === i)); rows.forEach((r, k) => r.classList.toggle('on', k === i)); mb.textContent = rows[i].dataset.p; ms.textContent = rows[i].dataset.t; };
  const off = () => { donut.classList.remove('dim'); segs.forEach(s => s.classList.remove('on')); rows.forEach(r => r.classList.remove('on')); mb.textContent = def[0]; ms.textContent = def[1]; };
  segs.forEach((s, i) => { s.addEventListener('mouseenter', () => on(i)); s.addEventListener('mouseleave', off); });
  rows.forEach((r, i) => { r.addEventListener('mouseenter', () => on(i)); r.addEventListener('mouseleave', off); r.addEventListener('click', () => on(i)); });
  new IntersectionObserver((es, o) => { if (es[0].isIntersecting) { segs.forEach(s => s.style.strokeDashoffset = s.dataset.off); o.disconnect(); } }, { threshold: .4 }).observe(donut);
}

/* reels: storyboard beats like stories, or the real video once MEDIA is set */
$$('.rv').forEach(rv => {
  const src = MEDIA[rv.dataset.key];
  if (src) { $('img.bg', rv).insertAdjacentHTML('afterend', `<video src="${src}" autoplay muted loop playsinline></video>`); $('.beat', rv).remove(); $('.bars', rv).remove(); return; }
  const beats = JSON.parse(rv.dataset.beats), bars = $('.bars', rv), box = $('.beat', rv);
  const imgs = JSON.parse(rv.dataset.imgs || '[]'), bg = $('img.bg', rv);
  imgs.forEach(u => { const im = new Image(); im.src = u; });
  bars.innerHTML = beats.map(() => '<i><b></b></i>').join('');
  let i = 0, timer = null;
  const show = () => { $$('i', bars).forEach((b, k) => { b.className = k < i ? 'done' : (k === i ? 'cur' : ''); });
    if (imgs[i] && !bg.src.endsWith(imgs[i])) { bg.classList.add('sw'); setTimeout(() => { bg.src = imgs[i]; bg.classList.remove('sw'); }, 250); }
    box.innerHTML = `<span>${beats[i]}</span>`; timer = setTimeout(() => { i = (i + 1) % beats.length; show(); }, 2800); };
  new IntersectionObserver(es => { if (es[0].isIntersecting) { if (!timer) show(); } else { clearTimeout(timer); timer = null; } }, { threshold: .4 }).observe(rv);
});

/* loop: walk the five steps */
const loop = $('.loop');
if (loop) {
  const nodes = $$('.node', loop), steps = $$('.steps li'); let k = 0, t = null;
  const go2 = () => { nodes.forEach((n, i) => n.classList.toggle('on', i === k)); steps.forEach((s, i) => s.classList.toggle('on', i === k)); k = (k + 1) % nodes.length; t = setTimeout(go2, 2600); };
  steps.forEach((s, i) => s.addEventListener('mouseenter', () => { clearTimeout(t); k = i; go2(); }));
  new IntersectionObserver(es => { if (es[0].isIntersecting) { if (!t) go2(); } else { clearTimeout(t); t = null; } }, { threshold: .3 }).observe(loop);
}

/* tickable lists */
$$('.chk li').forEach(c => { const t = () => c.classList.toggle('on'); c.addEventListener('click', t); c.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); t(); } }); });
