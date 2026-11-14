/* ===== Inovosense proposal site ===== */
/* Media swap: put the finished reels in the media/ folder and write their file names here. */
const MEDIA = {
  reel1: '',   // e.g. 'media/reel-labkhand.mp4'  — «لبخندمو دوست دارم»
  reel2: '',   // e.g. 'media/reel-qanat.mp4'     — «از قنات تا پوست»
  reel3: ''    // e.g. 'media/reel-jabe.mp4'      — «جعبه رو برگردون»
};

const FA = s => String(s).replace(/\d/g, d => '۰۱۲۳۴۵۶۷۸۹'[d]);
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

/* reveal + one-shot triggers */
const io = new IntersectionObserver(es => es.forEach(e => {
  if (!e.isIntersecting) return;
  const el = e.target; el.classList.add('in'); io.unobserve(el);
  if (el.dataset.count) count(el);
  if (el.id === 'bigq') typeQ(el);
  if (el.classList.contains('dm-b')) el.parentElement.classList.add('dm-in');
}), { threshold: .18, rootMargin: '0px 0px -6% 0px' });
$$('[data-r],[data-count],#bigq,.tl,.bud,.dm-b,.donut').forEach(el => io.observe(el));

function count(el) {
  const to = +el.dataset.count, dur = 1600, t0 = performance.now();
  const step = t => { const k = Math.min(1, (t - t0) / dur), v = Math.round(to * (1 - Math.pow(1 - k, 3)));
    el.textContent = FA(v); if (k < 1) requestAnimationFrame(step); };
  if (reduce) el.textContent = FA(to); else requestAnimationFrame(step);
}

function typeQ(el) {
  const span = $('.typed', el), full = span.dataset.t; let i = 0;
  if (reduce) { span.textContent = full; el.classList.add('done'); return; }
  span.textContent = '';
  const tick = () => { span.textContent = full.slice(0, ++i); if (i < full.length) setTimeout(tick, 55 + Math.random() * 50); else el.classList.add('done'); };
  setTimeout(tick, 400);
}

/* nav: solid on scroll, progress, active link */
const nav = $('.nav'), prog = $('.prog'), links = $$('.nav ul a');
const secs = links.map(a => $(a.getAttribute('href'))).filter(Boolean);
addEventListener('scroll', () => {
  const y = scrollY, h = document.documentElement.scrollHeight - innerHeight;
  nav.classList.toggle('solid', y > innerHeight * .7);
  prog.style.width = (y / h * 100) + '%';
  let cur = null; secs.forEach(s => { if (s.getBoundingClientRect().top < innerHeight * .4) cur = s; });
  links.forEach(a => a.classList.toggle('on', cur && a.getAttribute('href') === '#' + cur.id));
}, { passive: true });

/* hero: light follows the pointer + rising dust */
const hero = $('.hero');
hero.addEventListener('pointermove', e => { const r = hero.getBoundingClientRect();
  hero.style.setProperty('--mx', (e.clientX - r.left) + 'px'); hero.style.setProperty('--my', (e.clientY - r.top) + 'px'); });
const dust = $('.dust');
if (dust && !reduce) for (let i = 0; i < 26; i++) { const d = document.createElement('i');
  d.style.left = (30 + Math.random() * 40) + '%'; d.style.animationDuration = (9 + Math.random() * 10) + 's';
  d.style.animationDelay = (-Math.random() * 18) + 's'; d.style.transform = `scale(${.5 + Math.random()})`; dust.appendChild(d); }

/* drag-to-scroll strips */
$$('.strip').forEach(st => {
  let down = false, sx = 0, sl = 0, moved = 0;
  st.addEventListener('pointerdown', e => { if (e.pointerType !== 'mouse') return; down = true; moved = 0; sx = e.clientX; sl = st.scrollLeft; });
  addEventListener('pointermove', e => { if (!down) return; const dx = e.clientX - sx; moved = Math.abs(dx); if (moved > 4) st.classList.add('drag'); st.scrollLeft = sl - dx; });
  addEventListener('pointerup', () => { down = false; st.classList.remove('drag'); });
  const w = st.parentElement;
  $$('.sbtn button', w).forEach(b => b.addEventListener('click', () => st.scrollBy({ left: +b.dataset.dir * 380, behavior: 'smooth' })));
});

/* Instagram phone: open a post, swipe the carousel, double-tap like */
const POSTS = window.IG_POSTS || {};
const view = $('#igpost');
if (view) {
  const track = $('.track', view), dots = $('.dots', view), cnt = $('.cnt', view), cap = $('.cap', view), heart = $('.heart', view), lk = $('.lk', view);
  function openPost(id) {
    const p = POSTS[id]; if (!p) return;
    track.innerHTML = p.imgs.map(s => `<img src="${s}" alt="">`).join('');
    track.scrollLeft = 0;
    dots.innerHTML = p.imgs.length > 1 ? p.imgs.map((_, i) => `<i class="${i ? '' : 'on'}"></i>`).join('') : '';
    cnt.style.display = p.imgs.length > 1 ? '' : 'none'; cnt.textContent = FA(`1/${p.imgs.length}`);
    cap.innerHTML = `<b>inovosense</b>${p.cap}<span class="t">${p.time || 'نمونهٔ پیشنهادی'}</span>`;
    lk.classList.remove('on'); view.classList.add('open'); view.scrollTop = 0;
  }
  $$('.ig-grid button[data-p]').forEach(b => b.addEventListener('click', () => openPost(b.dataset.p)));
  $('.back', view).addEventListener('click', () => view.classList.remove('open'));
  track.addEventListener('scroll', () => {
    const n = track.children.length; if (n < 2) return;
    const i = Math.round(Math.abs(track.scrollLeft) / track.clientWidth);
    $$('i', dots).forEach((d, k) => d.classList.toggle('on', k === i)); cnt.textContent = FA(`${i + 1}/${n}`);
  }, { passive: true });
  let last = 0;
  track.addEventListener('pointerup', () => { const t = Date.now(); if (t - last < 320) { heart.classList.remove('pop'); void heart.offsetWidth; heart.classList.add('pop'); lk.classList.add('on'); } last = t; });
  lk.addEventListener('click', () => lk.classList.toggle('on'));
  // desktop: drag the carousel with the mouse
  let d = false, x0 = 0, s0 = 0;
  track.addEventListener('pointerdown', e => { if (e.pointerType !== 'mouse') return; d = true; x0 = e.clientX; s0 = track.scrollLeft; track.style.scrollSnapType = 'none'; });
  addEventListener('pointerup', () => { if (!d) return; d = false; track.style.scrollSnapType = ''; const w = track.clientWidth; track.scrollTo({ left: Math.round(track.scrollLeft / w) * w, behavior: 'smooth' }); });
  addEventListener('pointermove', e => { if (d) track.scrollLeft = s0 - (e.clientX - x0); });
  // auto-open the carousel once, as a hint
  const once = new IntersectionObserver(es => { if (es[0].isIntersecting) { setTimeout(() => openPost('f1'), 1400); setTimeout(() => { if (!reduce) track.scrollTo({ left: track.clientWidth, behavior: 'smooth' }); }, 2900); setTimeout(() => view.classList.remove('open'), 6500); once.disconnect(); } }, { threshold: .6 });
  once.observe(view.closest('.phone'));
}

/* before / after slider */
$$('.ba-frame').forEach(f => { const r = $('input', f); const set = () => f.style.setProperty('--p', r.value + '%'); r.addEventListener('input', set); set(); });

/* the card opens */
const lc = $('.lcard');
if (lc) { const t = () => lc.classList.toggle('open'); lc.addEventListener('click', t); $('.opencue').addEventListener('click', t);
  new IntersectionObserver((es, o) => { if (es[0].isIntersecting) { setTimeout(() => lc.classList.add('open'), 900); o.disconnect(); } }, { threshold: .7 }).observe(lc); }

/* donut ↔ list */
const donut = $('.donut');
if (donut) {
  const segs = $$('circle.s', donut), rows = $$('.sr'), mid = $('.mid', donut), mb = $('b', mid), ms = $('span', mid);
  const def = [mb.textContent, ms.textContent];
  const on = i => { donut.classList.add('dim'); segs.forEach((s, k) => s.classList.toggle('on', k === i)); rows.forEach((r, k) => r.classList.toggle('on', k === i)); mb.textContent = rows[i].dataset.p; ms.textContent = rows[i].dataset.t; };
  const off = () => { donut.classList.remove('dim'); segs.forEach(s => s.classList.remove('on')); rows.forEach(r => r.classList.remove('on')); mb.textContent = def[0]; ms.textContent = def[1]; };
  segs.forEach((s, i) => { s.addEventListener('mouseenter', () => on(i)); s.addEventListener('mouseleave', off); });
  rows.forEach((r, i) => { r.addEventListener('mouseenter', () => on(i)); r.addEventListener('mouseleave', off); });
  new IntersectionObserver((es, o) => { if (es[0].isIntersecting) { segs.forEach(s => s.style.strokeDashoffset = s.dataset.off); o.disconnect(); } }, { threshold: .4 }).observe(donut);
}

/* reels: storyboard beats like stories, or a real video if MEDIA is set */
$$('.rv').forEach(rv => {
  const key = rv.dataset.key, src = MEDIA[key];
  if (src) { rv.querySelector('img.bg').insertAdjacentHTML('afterend', `<video src="${src}" autoplay muted loop playsinline></video>`); $('.beat', rv).remove(); $('.bars', rv).remove(); return; }
  const beats = JSON.parse(rv.dataset.beats), bars = $('.bars', rv), box = $('.beat', rv);
  bars.innerHTML = beats.map(() => '<i><b></b></i>').join('');
  let i = 0, timer = null;
  const show = () => { $$('i', bars).forEach((b, k) => { b.className = k < i ? 'done' : (k === i ? 'cur' : ''); });
    box.innerHTML = `<span>${beats[i]}</span>`; timer = setTimeout(() => { i = (i + 1) % beats.length; show(); }, 2800); };
  new IntersectionObserver(es => { if (es[0].isIntersecting) { if (!timer) show(); } else { clearTimeout(timer); timer = null; } }, { threshold: .4 }).observe(rv);
});

/* loop: walk the five steps */
const loop = $('.loop');
if (loop) {
  const nodes = $$('.node', loop), steps = $$('.stp'); let k = 0, t = null;
  const go = () => { nodes.forEach((n, i) => n.classList.toggle('on', i === k)); steps.forEach((s, i) => s.classList.toggle('on', i === k)); k = (k + 1) % nodes.length; t = setTimeout(go, 2600); };
  steps.forEach((s, i) => s.addEventListener('mouseenter', () => { clearTimeout(t); k = i; go(); }));
  new IntersectionObserver(es => { if (es[0].isIntersecting) { if (!t) go(); } else { clearTimeout(t); t = null; } }, { threshold: .3 }).observe(loop);
}

/* tickable checklists */
$$('.ck').forEach(c => c.addEventListener('click', () => c.classList.toggle('on')));
