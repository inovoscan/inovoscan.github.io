# -*- coding: utf-8 -*-
# Inovosense · «از عمق تا نور» — proposal site, v2 (depth → light).
import json, html, math, random, html as H

FA = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
def fa(x): return str(x).translate(FA)
def en(t): return f'<span class="en">{t}</span>'
def a(url, label): return f'<a href="{url}" target="_blank" rel="noopener">{label}</a>'
C = dict(shine='#b4d235', silk='#f39a3c', smile='#e8325c', style='#6a2f97', shape='#3ec6cc')
K5 = ['shine', 'silk', 'smile', 'style', 'shape']

# ---------- icons ----------
I = dict(
 heart='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 20.5s-7.6-4.6-9.6-9.2C.9 7.7 3.2 4.5 6.6 4.5c2.1 0 3.6 1.1 4.4 2.5h2c.8-1.4 2.3-2.5 4.4-2.5 3.4 0 5.7 3.2 4.2 6.8-2 4.6-9.6 9.2-9.6 9.2Z"/></svg>',
 cmt='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M20.6 11.6a8.6 8.6 0 0 1-12.8 7.5L3.4 20.3l1.2-4.3a8.6 8.6 0 1 1 16-4.4Z"/></svg>',
 send='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M21.5 2.5 2.8 9.7l7.3 2.9 2.9 7.3z"/><path d="M21.5 2.5 10.1 12.6"/></svg>',
 save='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M6 3.5h12v17l-6-4.6-6 4.6z"/></svg>',
 grid='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><rect x="3" y="3" width="18" height="18" rx="1"/><path d="M9 3v18M15 3v18M3 9h18M3 15h18"/></svg>',
 reels='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><rect x="3" y="3" width="18" height="18" rx="4"/><path d="M3 8h18M8.5 3l3 5M14.5 3l3 5M10 11.3v6.2l5.2-3.1z"/></svg>',
 tag='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="12" cy="10" r="3"/><path d="M6.5 19c1-2.6 3-4 5.5-4s4.5 1.4 5.5 4"/></svg>',
 dots='<svg viewBox="0 0 24 24" fill="currentColor"><circle cx="5" cy="12" r="1.7"/><circle cx="12" cy="12" r="1.7"/><circle cx="19" cy="12" r="1.7"/></svg>',
 back='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 5l7 7-7 7"/></svg>',
 addp='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="10" cy="8" r="4"/><path d="M3 20c.8-3.6 3.6-5.5 7-5.5s6.2 1.9 7 5.5M19 8v6M16 11h6"/></svg>',
 multi='<svg class="ml" viewBox="0 0 24 24" fill="#fff"><path d="M7 3h11a3 3 0 0 1 3 3v11h-2V6a1 1 0 0 0-1-1H7z"/><rect x="3" y="7" width="14" height="14" rx="2.5"/></svg>',
 reelmark='<svg class="ml" viewBox="0 0 24 24" fill="#fff"><path d="M8 5.5v13l11-6.5z"/></svg>',
 clinic='<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M6 34V14l14-8 14 8v20z"/><path d="M16 34v-8h8v8M20 13v6M17 16h6"/></svg>',
 ext='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>',
)

def sbar(dark=False):
    return f'<div class="island"></div><div class="sbar{" dk" if dark else ""}"><span>۹:۴۱</span><span class="bt"><i></i><i></i><i></i><b></b></span></div>'

# ---------- Instagram phone (profile + post viewer) ----------
def ig_phone(pid, handle, name, cat, bio, stats, tiles, hl=None, avatar='', link='', back=True, extra_cls=''):
    """tiles: list of dicts {img, key, kind('post'|'car'|'reel')}"""
    av = f'<img src="{avatar}" alt="">' if avatar.startswith('img/') else f'<b>{avatar}</b>'
    top = (f'<div class="ig-top"><span class="ib">{I["back"]}</span><b class="u">{handle}</b><span class="ib">{I["dots"]}</span></div>' if back
           else f'<div class="ig-top"><span class="ib"></span><b class="u">{handle}</b><span class="ib">{I["dots"]}</span></div>')
    st = ''.join(f'<div><b>{v}</b><span>{k}</span></div>' for k, v in stats)
    hls = ''
    if hl:
        hls = '<div class="ig-hl">' + ''.join(f'<div><i style="--c:{c}"><span></span></i>{t}</div>' for t, c in hl) + '</div>'
    grid = ''.join(
        f'<button data-p="{t["key"]}" aria-label="باز کردن پست"><img src="{t["img"]}" alt="" loading="lazy">'
        f'{I["multi"] if t.get("kind")=="car" else (I["reelmark"] if t.get("kind")=="reel" else "")}</button>' for t in tiles)
    if not tiles:
        grid = '<div class="ig-empty">هنوز پستی منتشر نشده</div>'
    lk = f'<span class="lk">{link}</span>' if link else ''
    return f'''<div class="phone {extra_cls}" id="{pid}"><div class="scr">{sbar()}
  <div class="ig">{top}
    <div class="ig-head"><div class="ig-av"><span>{av}</span></div>
      <div class="ig-st">{st}</div></div>
    <div class="ig-bio"><b>{name}</b>{f'<em>{cat}</em>' if cat else ''}{bio}{lk}</div>
    <div class="ig-btns"><span class="f">دنبال کردن</span><span>پیام</span><span class="ic">{I["addp"]}</span></div>
    {hls}
    <div class="ig-tabs"><span class="on">{I['grid']}</span><span>{I['reels']}</span><span>{I['tag']}</span></div>
    <div class="ig-grid">{grid}</div>
  </div>
  <div class="ig-post">
    <div class="ph"><button class="back" aria-label="بازگشت">{I["back"]}</button><span class="av">{av}</span><span class="u">{handle}</span><span class="ib">{I["dots"]}</span></div>
    <div class="car"><div class="track"></div><span class="cnt"></span><svg class="heart" viewBox="0 0 24 24" fill="#fff"><path d="M12 21s-7.5-4.6-9.8-9.1C.6 8.5 2.6 4.5 6.4 4.5c2.3 0 3.8 1.3 4.6 2.6h2c.8-1.3 2.3-2.6 4.6-2.6 3.8 0 5.8 4 4.2 7.4C19.5 16.4 12 21 12 21Z"/></svg></div>
    <div class="act"><div class="dots"></div><span class="lkb">{I['heart']}</span>{I['cmt']}{I['send']}<span class="sv">{I['save']}</span></div>
    <div class="cap"></div>
  </div>
</div></div>'''

parts = []
def P(s): parts.append(s)

def chapter(n, title, line, img, color, zone):
    return f'''<section class="chap z-{zone}" style="--c:{color}">
  <div class="chap-img"><img src="{img}" alt="" loading="lazy"></div>
  <div class="chap-txt"><span class="chap-n">فصل {fa(n)}</span><i class="band"></i><h2>{title}</h2><p>{line}</p></div>
</section>'''

# ================= NAV + depth gauge =================
NAV = [('sentence','جمله'),('today','امروز'),('refs','مرجع‌ها'),('idea','ایده'),('card','کارت'),
       ('instagram','پیج'),('series','محتوا'),('films','فیلم‌ها'),('plan','اجرا'),('visibility','دیده‌شدن'),('next','تصمیم‌ها')]
P(f'''<nav class="nav"><a class="brand" href="#top"><img class="lg-l" src="img/logo_light.png" alt="INOVO SENSE"><img class="lg-d" src="img/logo_dark.png" alt="INOVO SENSE"></a>
<ul>{''.join(f'<li><a href="#{i}">{t}</a></li>' for i,t in NAV)}</ul></nav>
<div class="gauge" aria-hidden="true"><span class="g-t">نور</span><i><b></b></i><span class="g-b">عمق</span></div>''')

# ================= HERO =================
P(f'''<section class="hero z-d" id="top">
<div class="hbg"><img src="img/ai/qanat-corridor-11.jpg" alt=""></div><div class="hshade"></div><div class="beam"></div>
<div class="wrap hero-in">
  <div class="hero-t">
    <img class="logo" src="img/logo_light.png" alt="INOVO SENSE">
    <h1 class="slogan"><span>از عمق</span><span>تا نور</span></h1>
    <p class="sub">پروپوزال استراتژی اینستاگرام اینووسنس، برای {en('KMT')}.<br>چطور مردم خودشان از دکترشان اینووسنس را بخواهند.</p>
  </div>
  <div class="boxes">{''.join(f'<div class="bx" style="--c:{C[k]};--i:{n}"><img src="img/box_{k}.webp" alt="{k}"></div>' for n,k in enumerate(['silk','smile','shine','style','shape']))}</div>
</div>
<a class="down" href="#sentence" aria-label="ادامه">پایین بروید</a>
</section>''')

# ================= SENTENCE =================
P(f'''<section class="sec z-d sentence" id="sentence">
<div class="wrap">
  <p class="pre">مردم نباید اسم فیلر را حفظ کنند. باید یک جمله را حفظ کنند:</p>
  <div class="bigq" id="bigq"><span class="gm">«</span><span class="typed" data-t="دکتر، اینووسنس برای من مناسبه؟">دکتر، اینووسنس برای من مناسبه؟</span><span class="gm">»</span></div>
  <div class="ctas"><a href="#card" class="cta">کارت نقشهٔ نور را باز کن ↓</a><a href="#instagram" class="cta ghost">پیج پیشنهادی و فیلم شروع را ببین ↓</a></div>
  <div class="nums">
    <div><b data-count="1">۱</b><p>جمله‌ای که بیمار در مطب می‌گوید؛ هدف کل این پروپوزال.</p></div>
    <div><b data-count="100">۱۰۰</b><p>معیار موفقیت: در هر ۱۰۰ مشاوره، چند بار بیمار خودش اسم اینووسنس را می‌آورد.</p></div>
    <div><b class="w">صفر</b><p>ریال تبلیغ پولی متا. اعتبار این برند از مطب می‌آید، نه از آگهی.</p></div>
  </div>
</div></section>''')

# ================= TODAY (current page) =================
CUR = [{'img': f'img/ino_{i}.jpg', 'key': f'c{i}'} for i in range(9)]
CUR_POSTS = {f'c{i}': {'imgs': [f'img/ino_{i}.jpg'], 'cap': 'یکی از ۹ پست آخر پیج امروز اینووسنس.', 'url': 'https://www.instagram.com/inovosense/', 'ul': 'دیدن پیج در اینستاگرام'} for i in range(9)}
P(f'''<section class="sec z-d" id="today">
<div class="wrap split">
  <div class="txt">
    <h2>پیج امروز با پزشک‌ها حرف می‌زند، نه با مردم</h2>
    <dl class="facts">
      <div><dt>۱۹٫۷ هزار</dt><dd>دنبال‌کننده و ۱۹۷ پست در {a('https://www.instagram.com/inovosense/', en('@inovosense'))}.</dd></div>
      <div><dt>دو شعار</dt><dd>بیو می‌گوید «{en('Sense of Confidence')}»؛ «{en('From Depth to the Light')}» فقط زیر برند فرعی {en('INOVOLIFE')} و با لوگوی دیگری آمده.</dd></div>
      <div><dt>پنج سبک</dt><dd>در ۹ پست آخر، پنج زبان بصری متفاوت. هیچ پستی شبیه پست کنارش نیست.</dd></div>
      <div class="warn"><dt>«معجزه»</dt><dd>پست «ترمیم پوست با معجزهٔ {en('PDRN')}»: کلمهٔ ممنوع و ادعای درمانی. باید همین هفته برداشته شود.</dd></div>
      <div><dt>۳۷ از ۲۰۰</dt><dd>۳۷ پزشک در سایت فهرست شده‌اند، ولی ادعا ۲۰۰ پزشک است. بیمار باید بتواند پزشک واقعی را پیدا کند.</dd></div>
    </dl>
  </div>
  <div class="dev">{ig_phone('ph-today','inovosense','Inovosense','','<span class="en">Sense of Confidence</span>',[('پست','۱۹۷'),('دنبال‌کننده','۱۹٫۷ هزار'),('دنبال‌شونده','۱۲۰')],CUR,avatar='img/logo_dark.png')}
    <p class="hint">روی پست‌ها بزنید</p></div>
</div></section>''')

# ================= RULES + PHASE ZERO =================
rules = [('مجوز تبلیغ سیتا','مجوز نظام پزشکی برای هر اکانت و هر رسانه جدا گرفته می‌شود. بدون مجوز، هیچ پستی منتشر نمی‌شود.','shine'),
 ('بدون ادعای درمانی','طبق دستورالعمل جاری تبلیغات نظام پزشکی، تبلیغ کالای دارای ادعای درمانی برای عموم ممنوع است. ما «سؤال» و «فرایند» را می‌گوییم، نه «نتیجه» را.','silk'),
 ('بدون چهرهٔ مشهور و پزشک','تأیید محصول به‌دست سلبریتی ممنوع است. تبلیغ تجاری کالای پزشکی از زبان پزشک هم تخلف است.','smile'),
 ('بدون «برترین» و «معجزه»','«بهترین»، «برترین»، «معجزه»، «تضمینی» و «بی‌درد» از واژه‌نامهٔ برند حذف می‌شوند.','style')]
P(f'''<section class="sec z-d" id="rules">
<div class="wrap">
  <h2>پیش از هر ایده، چهار خط قرمز</h2>
  <ol class="rules">{''.join(f'<li style="--c:{C[c]}"><h3>{t}</h3><p>{d}</p></li>' for t,d,c in rules)}</ol>
  <div class="auth">
    <figure><img src="img/ai/box-hands-45.jpg" alt="" loading="lazy"><figcaption>نمونهٔ مفهومی؛ در تولید نهایی، جعبهٔ واقعی اینووسنس</figcaption></figure>
    <div>
      <h3>درِ ورود ما، یک توصیهٔ رسمی است</h3>
      <p>سازمان غذا و دارو به بیماران توصیه می‌کند پیش از تزریق دربارهٔ مجوز فرآورده بپرسند و برچسب اصالت ({en('TTAC')}) را ببینند. سری «جعبه رو برگردون» همین توصیه را به زبان مردم می‌گوید.</p>
      <h3 class="mt">مرحلهٔ صفر: درخواست مشخص، نه سؤال کلی</h3>
      <p>از مرجع تبلیغات نظام پزشکی مجوز سیتا برای پیج رسمی شرکت صاحب‌پروانه می‌خواهیم، با نام و لوگو، برای «آگاهی‌بخشی، اصالت‌سنجی و ایمنی، بدون ادعای درمانی و ترغیبی». سناریوی هر فیلم، کپشن‌ها و حساب انتشار جدا ضمیمه می‌شوند.</p>
      <ol class="ladder">
        <li><b>درخواست اصلی</b><span>محتوای کامل نقشهٔ نور، با نام و لوگو، بدون هیچ ادعا.</span></li>
        <li><b>اگر رد شد</b><span>همان پیج با نام برند، ولی فقط اصالت ({en('TTAC')}) و ایمنی.</span></li>
        <li><b>فقط اگر آن هم رد شد</b><span>نسخهٔ بی‌نام؛ نام اینووسنس روی کارت، روی جعبه و در مطب.</span></li>
      </ol>
      <h3 class="mt">سه ضمیمهٔ درخواست</h3>
      <ul class="plain dk"><li><b>پروانهٔ ساخت و کد {en('IRC')}</b> از سازمان غذا و دارو.</li><li><b>متن پیشنهادی بیو:</b> نام رسمی شرکت صاحب‌پروانه، شمارهٔ مجوز سیتا، و «صرفاً برای آگاهی‌بخشی و اصالت فرآورده».</li><li><b>درخواست تأیید قالب شش سری برای یک سال</b>، با نمونه‌سناریوهای فصل اول؛ تا هر پست جدا در صف کمیته نماند.</li></ul>
      <p class="note">در پلهٔ سوم، کارت باعث نمی‌شود بیمار در اول همان مشاوره اسم اینووسنس را ببرد، چون آخر مشاوره داده می‌شود. نقشش یادآوری و معرفی به نفر بعدی است: بیمار اسم را با خودش می‌برد و به دوستش می‌گوید. شمارهٔ ماده‌ها در نسخه‌های مختلف دستورالعمل فرق دارد؛ پیش از جلسه با متن رسمی جاری کنترل شود. این بخش جایگزین نظر مشاور حقوقی کارفرما نیست.</p>
    </div>
  </div>
</div></section>''')

# ================= CHAPTER 1 + REFERENCES BROWSER =================
P(chapter(1, 'از دیگران چه یاد می‌گیریم', '۱۸ برند که مردم اسمشان را صدا می‌زنند. روی هر برند بزنید تا پیجش در گوشی باز شود و تحلیل ما کنارش بیاید.', 'img/ai/box-flip-916.jpg', C['shine'], 'd'))

B = [
 dict(n='Hydrafacial',h='hydrafacial',f='۴۲۴ هزار',k='hydrafacial',w='https://www.hydrafacial.com',tag='نزدیک‌ترین الگو',
  why='یک «درمان» را به «اسم» تبدیل کرد. مشتری به کلینیک نمی‌گوید «پاکسازی عمیق می‌خواهم»، می‌گوید «هایدرافیشال می‌خواهم».',
  idea='روی سایت «مرکز تأییدشده پیدا کن» دارد. برنامهٔ سفیران متخصص پوست، کلینیک‌ها را شریک برند کرده.',
  les='نزدیک‌ترین الگو به هدف ماست: برندی که از راه کلینیک، اسم‌دار شده.',
  use='ریلز و هایلایت «اسم دکتر رو کجا چک کنم؟». فهرست مراکز، اگر کارفرما بخواهد، با عنوان «شرکت در دورهٔ اینووکادمی»، نه «پزشک تأییدشده».'),
 dict(n='Restylane',h='restylaneusa',f='۶۴ هزار',k='restylane',w='https://www.restylane.com',tag='رقیب هم‌ایده',
  why='شخصی‌سازی را پیش از ما گفته: «مشاوره‌ات، سؤال‌هایت؛ همه را بپرس» و «کدام بیمار رستیلین هستی؟».',
  idea='پرسیدن را تشویق می‌کند. پست‌ها تایپوگرافیک، تمیز و سرمه‌ای‌اند.',
  les='«شخصی‌سازی» به‌تنهایی متمایز نیست. تمایز ما باید در آیین باشد، نه در فناوری ژل.',
  use='سه سؤال و کارت نقشهٔ نور؛ چیزی که بیمار در دست می‌گیرد و رستیلین ندارد.'),
 dict(n='Profhilo',h='profhilo_sea',f='۱۵ هزار',k='profhilo',w='https://www.profhilo.com',tag='الگوی شهرت',
  why='پیج خودش کوچک است. شهرتش از بیمارها و کلینیک‌ها در تیک‌تاک آمد، و از یک اسم دسته: «مرطوب‌کنندهٔ تزریقی».',
  idea='پست‌های «پروفایلوی تقلبی / اصل» و «۳ ثانیه تا اینکه اصل بودنش را چک کنی».',
  les='مردم اسم یک دسته را به خاطر می‌سپارند، و اصالت‌سنجی محتوای پرطرفداری است.',
  use='سری «جعبه رو برگردون». معنای «عمق» برای ما «برنامهٔ هر نفر» است، نه لایه‌های بافت.'),
 dict(n='SkinCeuticals',h='skinceuticals',f='۲ میلیون',k='skinceuticals',w='https://www.skinceuticals.com',tag='برند پزشک‌محور',
  why='فقط از راه پزشک فروخته می‌شود و با این حال سینمایی و خواستنی است: نور تیز، محصول وسط قاب.',
  idea='الان PDRN را معرفی می‌کند: اول یک صفحهٔ آموزشی «PDRN چیست» که تزریق در مطب و مراقبت خانگی را جدا می‌کند، بعد تیزر بی‌چهرهٔ «به‌زودی»، بعد لیست انتظار.',
  les='آگاهی‌سازی پیش از فروش، و پزشک همیشه وسط ماجرا.',
  use='«پزشکی» یعنی خشک نیست. پست‌های محصول‌محور با یک جمله، بدون ادعای برتری.'),
 dict(n='JUVÉDERM',h='juvederm',f='۵۱۸ هزار',k='juvederm',w='https://www.juvederm.com',tag='از سبد KMT',
  why='آموزش ساده و هایلایت ایمنی که همیشه در دسترس است.',
  use='هایلایت ثابت «اصالت و ایمنی». در محتوا هیچ محصولی از سبد KMT با دیگری مقایسه نمی‌شود.'),
 dict(n='rhode',h='rhode',f='رشد انفجاری',k='rhode',w='https://www.rhodeskin.com',tag='شیء دست‌به‌دست‌شدنی',
  why='سه محصول در شروع، یک عبارت حسی و یک شیء خواستنی: قاب گوشی‌ای که ۲۰۰ هزار نفر در صفش بودند.',
  use='مردم یک «عبارت» و یک «شیء» را دست‌به‌دست می‌کنند. شیء ما کارت نقشهٔ نور است.'),
 dict(n='Glossier',h='glossier',f='۳٫۱ میلیون',k='glossier',w='https://www.glossier.com',tag='یک باور، یک جمله',
  why='یک باور در یک جمله: «اول پوست، بعد آرایش». جامعه‌ای ساخت که حرف برند را تکرار می‌کند.',
  use='باور ما در یک جمله: «اول نقشه، بعد تزریق».'),
 dict(n='LANEIGE',h='laneige_us',f='۱٫۶ میلیون',k='laneige_us',w='https://us.laneige.com',tag='رنگ یعنی حافظه',
  why='یک محصول قهرمان با طعم‌ها و رنگ‌های جدا. رنگ، حافظهٔ برند شد.',
  use='رنگ نوار جعبه‌های اینووسنس زبان بصری پیج می‌شود.'),
 dict(n='Anua',h='anua_global',f='۸۱۴ هزار',k='anua_global',w='https://anua.com',tag='اول یک قهرمان',
  why='یک جزء قهرمان آن‌قدر تکرار شد که با خود برند یکی شد.',
  idea='برای PDRN شمارش معکوس «۱۲۰ ساعت» و هایلایت ماهی دارد؛ هیجان، نه پزشک.',
  use='سال اول با یک دسته جلو می‌رویم: «آب و نور پوست».'),
 dict(n='SK-II',h='skii',f='۴۵۴ هزار',k='skii',w='https://www.sk-ii.com',tag='داستان مبدأ',
  why='افسانهٔ مبدأ «پیترا»؛ پنجاه سال است همین داستان را می‌گوید.',
  use='داستان مبدأ بومی ما: قنات. آب از عمق، با نقشه، به نور می‌رسد.'),
 dict(n='Tatcha',h='tatcha',f='۱٫۴ میلیون',k='tatcha',w='https://www.tatcha.com',tag='آیین، با زبان امروز',
  why='آیین زیبایی ژاپنی را با زبان امروز روایت می‌کند.',
  use='گره‌چینی، کاشی و قنات، با زبان مینیمال امروز؛ ایرانی، ولی نه کهنه.'),
 dict(n='Sulwhasoo',h='sulwhasoo.official',f='۲۶۲ هزار',k='sulwhasoo',w='https://www.sulwhasoo.com',tag='لوکس از راه فرهنگ',
  why='شصت سال میراث، با معماری و صنایع‌دستی کره.',
  use='جزئیات صنایع‌دستی ایرانی، نه طلا و زرق‌وبرق.'),
 dict(n='Beauty of Joseon',h='beautyofjoseon_official',f='۱٫۴ میلیون',k='beautyofjoseon',w='https://beautyofjoseon.com',tag='میراث + یک قهرمان',
  why='از ۸۳ هزار دلار فروش در ۲۰۲۰ به ۱۱۶٫۷ میلیون دلار در ۲۰۲۳؛ با میراث و یک محصول قهرمان.',
  use='اثبات اینکه «میراث + یک قهرمان» برای برند غیرغربی کار می‌کند.'),
 dict(n='medicube',h='medicube_global_official',f='۱٫۹ میلیون',k='medicube',w='https://medicube.us',tag='محتوای زیاد و واقعی',
  why='«نتیجهٔ واقعی» و حجم بالای تولیدکنندهٔ محتوا.',
  use='محتوای زیاد و واقعی؛ ولی قبل‌وبعد و چهرهٔ مشهور در ایران پرریسک‌اند.'),
 dict(n='Shiseido',h='shiseido',f='۱٫۵ میلیون',k='shiseido',w='https://www.shiseido.com',tag='۱۵۰ سال علم',
  why='۱۵۰ سال «علم زندگی» و قرمز امضاشده.',
  use='پست‌هایی که چهرهٔ مشهور دارند را نیاوردیم و با لینک اینستاگرام جایشان گذاشتیم.'),
 dict(n='The Ordinary',h='theordinary',f='۳ میلیون',k='theordinary',w='https://theordinary.com',tag='شفافیت',
  why='«فرمول‌های بالینی با صداقت». شفافیت، خودش برند است.',
  use='لحن «لازم نیست» ما از همین جنس است.'),
 dict(n='La Mer',h='lamer',f='۱٫۲ میلیون',k='lamer',w='https://www.cremedelamer.com',tag='داستان، قیمت را توجیه می‌کند',
  why='افسانهٔ دانشمندی که برای سوختگی صورت خودش کرم ساخت. شعارش: «زاده از دریا».',
  idea='سری «سفر دست‌به‌دست»: از جنگل جلبک‌های عمق دریا تا آزمایشگاه و کنترل کیفیت؛ پشت صحنهٔ ساخت، بدون یک چهره.',
  les='نزدیک‌ترین مرجع برای جهان «دریا» و سری پشت صحنهٔ ساخت ما.',
  use='داستان قنات و دریا همین نقش را برای ما بازی می‌کند: عمق، دست، دقت.'),
 dict(n='Jeuveau',h='evolus',f='',k='jeuveau',w='https://www.jeuveau.com',tag='روز مخصوص برند',
  why='پیج خود جوو‌و خالی است؛ همه‌چیز در پیج شرکت مادر (اوولوس) است. یک «روز جوو‌و» در سال ساخته: ۱۱ نوامبر، با تخفیف در همهٔ کلینیک‌ها.',
  idea='یک روز مخصوص برند در تقویم، که کلینیک‌ها و بیمارها با هم جشنش می‌گیرند.',
  use='شهرت می‌تواند بیرون از پیج ساخته شود: در کلینیک، با یک روز مشترک.'),
]
REF_POSTS = {}
IGD = '/home/claude/prop/ig/'
NO_WEB = {'rhode','medicube','beautyofjoseon'}
BRANDS = []
for i, b in enumerate(B):
    d = json.load(open(IGD + b['k'] + '.json', encoding='utf-8'))
    url = f'https://www.instagram.com/{b["h"]}/' if b['h'] else ''
    b['url'] = url
    if d.get('f'): b['f'] = d['f']
    tiles = []
    for j, t in enumerate(d['tiles']):
        if t['img']:
            key = f'r{i}_{j}'
            cap = html.escape(t['cap'] or '')
            REF_POSTS[key] = {'imgs': [t['img']], 'cap': f'<span class="en orig">{cap}</span><br><span class="note">یادداشت ما:</span> {b["use"]}', 'url': t['href'], 'ul': 'دیدن همین پست در اینستاگرام', 'h': b['h']}
            tiles.append({'img': t['img'], 'key': key, 'kind': t['kind']})
        else:
            tiles.append({'href': t['href'], 'kind': t['kind']})
    web = f'img/web/{b["k"]}.jpg' if b['k'] not in NO_WEB else ''
    BRANDS.append({'n': b['n'], 'h': b['h'], 'f': b['f'], 'url': url, 'tag': b['tag'], 'why': b['why'], 'idea': b.get('idea',''), 'les': b.get('les',''), 'use': b['use'],
                   'hl': d.get('hl', [])[:6], 'tiles': tiles, 'web': web, 'w': b['w']})
b0 = B[0]
ref_phone = ig_phone('ph-ref', b0['h'], b0['n'], b0['tag'], '', [('دنبال‌کننده', b0['f'])], [t for t in BRANDS[0]['tiles'] if 'img' in t], avatar=b0['n'][0], link=f'instagram.com/{b0["h"]}')
P(f'''<section class="sec z-d refs" id="refs">
<div class="wrap browser">
  <ul class="blist" role="tablist">{''.join(f'<li><button role="tab" data-b="{i}" class="{"on" if i==0 else ""}"><span class="en">{b["n"]}</span><small>{b["tag"]}</small></button></li>' for i,b in enumerate(B))}</ul>
  <div class="bdev">{ref_phone}<a class="golink" href="{b0['url']}" target="_blank" rel="noopener">{I['ext']}<span>دیدن پیج در اینستاگرام</span></a></div>
  <article class="bnote">
    <span class="btag">{b0['tag']}</span>
    <h3 class="en bname">{b0['n']}</h3>
    <dl>
      <div><dt>چرا موفق شد</dt><dd data-k="why">{b0['why']}</dd></div>
      <div data-w="idea"><dt>ایده‌شان</dt><dd data-k="idea">{b0['idea']}</dd></div>
      <div data-w="les"><dt>درس برای ما</dt><dd data-k="les">{b0['les']}</dd></div>
      <div class="use"><dt>چطور استفاده کنیم</dt><dd data-k="use">{b0['use']}</dd></div>
    </dl>
    <a class="webcard" href="{BRANDS[0]['w']}" target="_blank" rel="noopener"><span class="wb"><i></i><i></i><i></i><em class="en">{BRANDS[0]['w'].replace('https://','')}</em></span><img src="{BRANDS[0]['web']}" alt="صفحهٔ اول سایت" loading="lazy"><span class="wt">صفحهٔ اول سایت برند {I['ext']}</span></a>
  </article>
</div>
<p class="wrap note">تصویرها فقط برای تحلیل داخلی‌اند و پست‌هایی که چهرهٔ آدم مشهور یا اینفلوئنسر دارند تصویرشان نیامده و فقط لینکشان هست. ۱۲ پست آخر هر پیج و صفحهٔ اول سایت‌ها: ۲۴ آبان ۱۴۰۵.</p>
</section>''')

lessons = [('اسم دسته، نه فقط اسم برند','Profhilo · Hydrafacial'),('یک جملهٔ قابل‌تکرار','Glossier · rhode'),('یک شیء دست‌به‌دست‌شدنی','rhode'),
 ('سیستم رنگ یعنی حافظه','LANEIGE'),('داستان مبدأ بومی','SK-II · Tatcha · Sulwhasoo · Beauty of Joseon'),('اصالت‌سنجی، خودش محتواست','Profhilo · Hydrafacial'),('مطب، کانال اصلی اعتماد','Hydrafacial · SkinCeuticals · Restylane')]
P(f'''<section class="sec z-d lessons-sec">
<div class="wrap">
  <h2>هفت درسی که برمی‌داریم</h2>
  <ol class="lessons">{''.join(f'<li><span class="t">{t}</span><span class="b en">{b}</span></li>' for t,b in lessons)}</ol>
</div></section>
<div class="tr tr-dm"></div>''')

# ================= CHAPTER 2: THE IDEA =================
P(chapter(2, 'نقشهٔ نور', 'ایده، تمایز، محصولات، داستان مبدأ و کارت.', 'img/ai/abanbar-916.jpg', C['silk'], 'm'))
P(f'''<section class="sec z-m idea" id="idea">
<div class="wrap">
  <h2 class="xl">پیش از هر تزریق، یک نقشه</h2>
  <p class="lead">دکتر طبق پروتکل اینووسنس برای همان بیمار نقشه می‌کشد. نقشه به سه سؤال جواب می‌دهد:</p>
  <ol class="q3">
    <li style="--c:{C['shine']}"><span class="qn">۱</span><h3>چرا این محصول؟</h3><p>از محصولات اینووسنس، کدام برای پوست و بافت من؟</p></li>
    <li style="--c:{C['smile']}"><span class="qn">۲</span><h3>چرا اینجا؟</h3><p>کدام ناحیه، و چرا نه جای دیگر؟</p></li>
    <li style="--c:{C['style']}"><span class="qn">۳</span><h3>چرا این مقدار؟</h3><p>چقدر، و در چند جلسه؟</p></li>
  </ol>
  <p class="answers">جواب صادقانه می‌تواند «بله» باشد، «فعلاً نه»، «گزینهٔ دیگری»، یا <b>«اصلاً لازم نیست»</b>. همین صداقت اعتبار می‌سازد.</p>
</div></section>
<div class="tr tr-ml"></div>''')

# the card (moved right after the idea)
P(f"""<section class="sec z-l cardsec" id="card">
<div class="wrap split">
  <div class="txt">
    <h2>کارت نقشهٔ نور</h2>
    <p class="lead">کارتی تاشو که دکتر آخر مشاوره می‌دهد، حتی اگر تصمیم امروز «فکر می‌کنم» باشد. جملهٔ خود مراجعه‌کننده بالای کارت می‌نشیند، و پیشنهاد پزشک در یک خط کوتاه زیرش: چه محصولی، کجا، چقدر، و چرا.</p>
    <ul class="plain">
      <li><b>بالای کارت، به خط خودش:</b> چیزی که برایش مهم است، در یک جمله.</li>
      <li><b>یک خط، سه «چرا»:</b> محصول، ناحیه و مقدار، با دلیل. کوتاه، تا پر کردنش وقت پزشک را نگیرد. «لازم نیست» هم جواب است.</li>
      <li><b>تصمیم امروز:</b> «تزریق»، «فعلاً نه»، «فکر می‌کنم». کسی که کاری نکرده هم دلیلی برای نگه‌داشتن کارت دارد.</li>
      <li><b>برچسب دوم سرنگ و کد {en('TTAC')}</b> روز تزریق داخلش چسبانده می‌شود؛ بیرونش ساده و بی‌نام، با نقش گره برجسته. دو نمونه را با دکمه‌های بالای کارت ببینید.</li>
    </ul>
    <p class="note">این نمونه، کارت همان زن فیلم «لبخندمو دوست دارم» است. جواب‌های پزشک فقط داخل کارت و در همین پروپوزال دیده می‌شوند؛ در پست‌های عمومی، کارت خالی یا فقط با جملهٔ خود مراجعه‌کننده نشان داده می‌شود.</p>
    <button class="opencue" type="button">باز کردن کارت</button>
  </div>
  <div class="cardbox">
    <div class="cstates" role="group" aria-label="دو نمونهٔ کارت"><button type="button" data-s="a" class="on">نمونهٔ ۱: تصمیم به تزریق</button><button type="button" data-s="b">نمونهٔ ۲: می‌خواهم فکر کنم</button></div>
    <div class="lcard">
      <div class="inside">
        <div class="mine"><span>چیزی که برای من مهم است</span><b>دلم می‌خواد وقتی می‌خندم، همین‌جوری بمونه.</b></div>
        <div class="f"><span>پیشنهاد پزشک و دلیلش</span><b>{en('Mesocell Plus')} برای کیفیت پوست گونه، نه خط لبخند؛ یک سرنگ کامل؛ خنده دست نمی‌خورد.</b></div>
        <div class="tks"><em>تصمیم امروز</em><span class="sa"><i></i>تزریق</span><span><i></i>فعلاً نه</span><span class="sb"><i></i>فکر می‌کنم</span></div>
        <div class="rw"><span>جلسه</span><b class="xa">۱ از ۳؛ جلسهٔ بعد چهار هفتهٔ دیگر</b><b class="xb">هر وقت تصمیم گرفتی؛ همین کارت را بیاور</b></div>
        <div class="lab xa"><span>برچسب سرنگ و کد {en('TTAC')}</span><i></i></div>
        <div class="lab empty xb"><span>جای برچسب سرنگ و کد {en('TTAC')}، برای روز تزریق</span></div>
      </div>
      <div class="cover"><img src="img/ai/card-emboss-43.jpg" alt=""></div>
    </div>
  </div>
</div>
<div class="wrap cphotos">
  <figure><img src="img/ai/box-card-tea-45.jpg" alt="" loading="lazy"><figcaption>بعد از مشاوره، در خانه</figcaption></figure>
  <figure><img src="img/ai/card-write-916.jpg" alt="" loading="lazy"><figcaption>پزشک جواب‌ها را می‌نویسد؛ فقط داخلی، در تبلیغ نمی‌آید</figcaption></figure>
  <p class="note">نوشته‌های روی کارت و عکس‌ها نمونهٔ مفهومی‌اند.</p>
</div>
</section>""")

P(f'''<section class="sec z-l" id="diff">
<div class="wrap">
  <h2>شبیه هیچ‌کدام نیستیم</h2>
  <div class="tblw"><table class="cmp">
  <thead><tr><th></th><th class="en">Profhilo</th><th class="en">Restylane</th><th class="us">اینووسنس</th></tr></thead>
  <tbody>
  <tr><th>معنای «عمق»</th><td>لایه‌های بافت؛ «از سطح تا ساختار عمقی»</td><td>—</td><td class="us">برنامهٔ هر نفر؛ از اولین سؤال تا آخرین جلسه</td></tr>
  <tr><th>شخصی‌سازی با</th><td>یک پروتکل ثابت برای همه</td><td>فناوری ژل</td><td class="us">آیین: سه سؤال، کارت، پروتکل پزشک</td></tr>
  <tr><th>چیزی که بیمار در دست دارد</th><td>—</td><td>—</td><td class="us">کارت نقشهٔ نور، با برچسب سرنگ و کد اصالت</td></tr>
  <tr><th>جملهٔ بیمار</th><td>«پروفایلو می‌خواهم»</td><td>«کدام رستیلین؟»</td><td class="us">«دکتر، اینووسنس برای من مناسبه؟»</td></tr>
  </tbody></table></div>
  <p class="note">ما ادعای «بهتر بودن» نمی‌کنیم و نام هیچ رقیبی را در محتوا نمی‌آوریم. این جدول فقط برای تیم داخلی است.</p>

  <h2 class="mt2">سه طبقه، به زبان مردم</h2>
  <div class="tiers">
    <div class="tier" style="--c:{C['shine']}"><div class="stage"><img src="img/cut_shine.webp" alt="Shine"></div><h3>آب و نور پوست</h3><p>کیفیت پوست، آب‌رسانی و درخشش. قهرمان سال اول.</p><p class="pn en">Shine · Shine Exo Plus · Mesocell Plus</p></div>
    <div class="tier" style="--c:{C['smile']}"><div class="stage"><img src="img/box_silk.webp" alt="Silk"><img src="img/box_smile.webp" alt="Smile"></div><h3>حرکت و ظرافت</h3><p>لب، لبخند و خطوطی که با حالت چهره حرکت می‌کنند.</p><p class="pn en">Silk · Smile</p></div>
    <div class="tier" style="--c:{C['style']}"><div class="stage"><img src="img/box_style.webp" alt="Style"><img src="img/box_shape.webp" alt="Shape"></div><h3>عمق و تکیه‌گاه</h3><p>حجم و ساختار؛ گونه، چانه و خط فک.</p><p class="pn en">Style · Shape</p></div>
  </div>
  <p class="note">رنگ نوار هر جعبه، کد آن محصول در کل پیج است. مردم اسم ژل را حفظ نمی‌کنند؛ رنگ را به یاد می‌آورند. محصول پوست سر ({en('Scalp Exo Plus')}) به خواست کارفرما بیرون از دامنهٔ این پروپوزال است.</p>
</div></section>''')

# qanat (animated section)
W, Hh, G = 1600, 760, 260
def chy(x): return 330 + (x-200)*(400/1400)
shafts = [520, 820, 1120, 1420]
sh = ''.join(f'<g><rect x="{x-14}" y="{G}" width="28" height="{chy(x)-G:.0f}" fill="#f7f2e9"/><path d="M{x-14} {G} V{chy(x):.0f} M{x+14} {G} V{chy(x):.0f}" stroke="#3a342b" stroke-width="1.6"/><ellipse cx="{x}" cy="{G}" rx="36" ry="8" fill="#c9b99c"/><polygon class="qbeam" points="{x-12},{G} {x+12},{G} {x+36},{chy(x):.0f} {x-36},{chy(x):.0f}" fill="url(#qb)" style="animation-delay:{-k*0.9}s"/></g>' for k,x in enumerate(shafts))
motes = ''.join(f'<circle class="qmote" cx="{820+random.Random(i).randint(-26,26)}" cy="{chy(820)-10:.0f}" r="{random.Random(i+9).choice([2,2.5,3])}" fill="#fff" style="animation-delay:{i*0.55:.2f}s"/>' for i in range(9))
strata = ''.join(f'<path d="M0 {y} Q400 {y+12} 800 {y+3} T1600 {y+8}" stroke="#a8946f" stroke-width="1.1" fill="none" opacity=".3"/>' for y in range(320, 760, 52))
qpath = f'M{W} {chy(W):.0f} L200 {chy(200):.0f} Q170 {chy(200)-30:.0f} 150 {G}'
qsvg = f'''<svg viewBox="0 0 {W} {Hh}" role="img" aria-label="قنات: آب از عمق زمین با نقشه به نور می‌رسد">
<defs>
<linearGradient id="qe" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e2d5bf"/><stop offset="1" stop-color="#bba584"/></linearGradient>
<linearGradient id="qb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffef6"/><stop offset="1" stop-color="#fffef6" stop-opacity=".15"/></linearGradient>
<linearGradient id="qw" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#14686e"/><stop offset="1" stop-color="#8fe9eb"/></linearGradient>
<radialGradient id="qg" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#fff"/><stop offset=".3" stop-color="#d6f7f8" stop-opacity=".9"/><stop offset="1" stop-color="#3ec6cc" stop-opacity="0"/></radialGradient>
</defs>
<rect y="{G}" width="{W}" height="{Hh-G}" fill="url(#qe)"/>{strata}{sh}
<path d="{qpath}" stroke="#2a2620" stroke-width="40" stroke-linecap="round" fill="none" opacity=".12"/>
<path d="{qpath}" stroke="url(#qw)" stroke-width="12" stroke-linecap="round" fill="none"/>
<path class="qflow" d="{qpath}" stroke="#e9ffff" stroke-width="3.5" stroke-linecap="round" fill="none" opacity=".85"/>
<circle class="qglow" cx="820" cy="{chy(820):.0f}" r="120" fill="url(#qg)"/>{motes}
<ellipse cx="160" cy="{G}" rx="110" ry="14" fill="#5fd0d4"/><ellipse cx="160" cy="{G-2}" rx="70" ry="7" fill="#c9f4f5"/>
<line x1="0" y1="{G}" x2="{W}" y2="{G}" stroke="#3a342b" stroke-width="2"/>
{''.join(f'<path d="M{x} {G} C{x-22} {G-36} {x-14} {G-h+36} {x} {G-h} C{x+14} {G-h+36} {x+22} {G-36} {x} {G}Z" fill="#2f4a33"/>' for x,h in [(70,190),(118,240),(165,175)])}
<text x="{W-60}" y="{Hh-60}" text-anchor="end" font-family="Estedad" font-size="34" font-weight="300" fill="#3a342b">عمق</text>
<text x="300" y="{G-30}" font-family="Estedad" font-size="34" font-weight="300" fill="#3a342b" text-anchor="middle">نور</text>
</svg>'''
P(f'''<section class="sec z-l qanat" id="qanat">
<div class="wrap split rev">
  <div class="txt">
    <h2>قنات</h2>
    <p class="lead">قنات، آب را از عمق زمین، با حساب و مهندسی، آرام به سطح می‌رساند تا باغ سبز شود. هیچ‌چیزش اتفاقی نیست: هر چاه جای خودش را دارد و هر شیب اندازهٔ خودش را.</p>
    <p class="lead strong">اینووسنس هم همین است: از عمق تا نور، با نقشه.</p>
    <p class="note">این داستان، ستون فیلم برند و هویت بصری است؛ با نور روشن و سنگ گرم روایت می‌شود، نه با تونل تاریک.</p>
  </div>
  <figure class="tall"><img src="img/ai/qanat-corridor-11.jpg" alt="" loading="lazy"><figcaption>نمونهٔ مفهومی: نور از بالا، آب در عمق</figcaption></figure>
</div>
<div class="qsvg">{qsvg}</div>
</section>''')

# ================= CHAPTER 3: CONTENT =================
P(chapter(3, 'محتوا', 'پیج پیشنهادی، شش سری ثابت، سه پست دایرکت‌فرست و سه فیلم اصلی.', 'img/ai/mirror-916.jpg', C['smile'], 'l'))

CAP = {
 'p5':'برای دوستی بفرست که فردا وقت مشاوره دارد. پرسیدن، حق اوست.',
 'p6':'پنج رنگ، پنج کار. اسم ژل را لازم نیست حفظ کنی؛ رنگش یادت بماند.',
 'p7':'شمارهٔ نظام پزشکی را بپرس و در سامانهٔ رسمی ببین. برای هر مراجعه‌ای به کار می‌آید.',
 'p2':'طبقهٔ اول نقشهٔ نور: آب و نور پوست. رنگ لیمویی یعنی همین.',
 'p8':'این سؤال‌ها بی‌احترامی نیست؛ مراقبت است. بفرست برای کسی که وقت گرفته.',
 'p9':'قنات، آب را با نقشه به نور می‌رساند. اینووسنس هم.',
 'f4':'کارتی که بعد از مشاوره می‌گیری، «چرا» را نگه می‌دارد؛ برچسب سرنگ هم داخلش است. تا جلسهٔ بعد نگهش دار.',
 'f1':'سه سؤال، پیش از هر تزریق. ورق بزن و ذخیره کن.',
 'f3':'اگر یکی از این جمله‌ها را شنیدی، دوباره بپرس. قبل از تزریق، ۱۵ ثانیه وقت بگذار.',
}
CAR = {'f4':['f4','p4'], 'f1':['f1','p1b','p1c','p1d','p1e'], 'f3':['f3','p3']}
ORDER = ['f4','p5','f1','p6','p9','p2','f3','p8','p7']
NEW_POSTS = {k: {'imgs': [f'img/posts/{x}.jpg' for x in CAR.get(k,[k])], 'cap': CAP[k] + ' <span class="hs">#نقشه_نور</span>', 'h': 'inovosense'} for k in ORDER}
NEW_TILES = [{'img': f'img/posts/{k}.jpg', 'key': k, 'kind': 'car' if k in CAR else 'post'} for k in ORDER]
hl = [('اصالت',C['shape']),('نقشهٔ نور',C['shine']),('سؤال‌ها',C['smile']),('قنات',C['style']),('کارت',C['silk'])]
bio = 'پیش از تزریق، سه سؤال بپرس.<br>اصالت: برچسب پشت جعبه.<br>نقشهٔ نور، در مطب پزشکت.'
new_phone = ig_phone('ph-new','inovosense','اینووسنس | از عمق تا نور','',bio,[('پست','۲۰۶'),('دنبال‌کننده','۱۹٫۷ هزار'),('دنبال‌شونده','۱۲۰')],NEW_TILES,hl=hl,avatar='img/logo_dark.png',link='inovosense.com',back=False,extra_cls='big')
old_grid = ''.join(f'<div><img src="img/ino_{i}.jpg" alt="" loading="lazy"></div>' for i in range(9))
new_grid = ''.join(f'<div><img src="img/posts/{k}.jpg" alt="" loading="lazy"></div>' for k in ORDER)
P(f'''<section class="sec z-l igsec" id="instagram">
<div class="wrap split">
  <div class="txt">
    <h2>نُه پست کنار هم، یک خانواده</h2>
    <p class="lead">این پیج پیشنهادی است، همان‌طور که در گوشی دیده می‌شود. روی پست‌ها بزنید تا باز شوند؛ سه پست کاروسل‌اند و ورق می‌خورند. دو بار ضربه بزنید، لایک می‌شود.</p>
    <ul class="plain">
      <li><b>یک در میان:</b> همیشه یک پست روشن و عکس‌دار، بعد یک پست به رنگِ روشن‌شدهٔ همان محصول، با نوار رنگ کامل پایینش. گرید سه‌ستونه با این قاعده شطرنجی می‌ماند، حتی وقتی پست‌ها یکی‌یکی منتشر شوند.</li>
      <li><b>نیمی طراحی، نیمی عکس:</b> جعبه و سرنگ واقعی، نور تراورتن، نقش گره‌چینی کم‌رنگ.</li>
      <li><b>یک جمله روی هر پست.</b> سه پست برای «ذخیره»، سه پست برای «فرستادن در دایرکت».</li>
    </ul>
    <div class="swatch">{''.join(f'<i style="--c:{C[k]}" title="{k}"></i>' for k in K5)}</div>
  </div>
  <div class="dev">{new_phone}<p class="hint">روی پست‌ها بزنید</p></div>
</div>
<div class="wrap ba-wrap">
  <h3 class="ba-h">قبل و بعد: دستگیره را بکشید</h3>
  <div class="ba-frame" style="--p:50%">
    <div class="layer"><div class="g9">{new_grid}</div></div>
    <div class="layer top"><div class="g9">{old_grid}</div></div>
    <span class="lab l">پیشنهاد</span><span class="lab r">امروز</span>
    <div class="knob"></div><input type="range" min="0" max="100" value="50" aria-label="مقایسهٔ پیج امروز و پیشنهادی">
  </div>
</div>
</section>''')

# series donut
series = [('چرا این، برای من؟','سه سؤال نقشهٔ نور را باز می‌کند؛ هر پست یک سؤال، بدون وعدهٔ نتیجه.','کاروسل، هفته‌ای ۱',25,C['shine']),
 ('جعبه رو برگردون','اصالت‌سنجی در ۱۵ ثانیه: برچسب، شمارهٔ ردیابی، پاسخ استعلام.','ریلز کوتاه، هفته‌ای ۱',20,C['shape']),
 ('ویس قبل ویزیت','از زبان مراجعه‌کننده و دوستش، نه پزشک؛ جمله‌هایی که می‌شود قرض گرفت و در دایرکت فرستاد.','ریلز و استوری، هفته‌ای ۲',20,C['silk']),
 ('سؤالی که نزدیک بود نپرسم','روایت بیمار واقعی (با رضایت کتبی) از سؤالی که برنامه‌اش را عوض کرد.','کاروسل متنی، دو هفته یک',15,C['smile']),
 ('از قنات تا پوست','فیلم برند و فرهنگ: نقشه، صبر، دقت.','ریلز سینمایی، ماهی ۱',10,C['style']),
 ('پشت صحنهٔ ساخت','سه محور گردشی: اتاق تمیز و پر شدن سرنگ، سفر برچسب اصالت تا روی جعبه، و گواهی‌های کنترل کیفیت مدیسا آرا گستر. بدون پزشک، بدون ادعا.','ریلز مستند، دو هفته یک',10,'#b48a52')]
R = 150; CIRC = 2*math.pi*R; acc = 0; segs = ''
for t,d,f,p,c in series:
    ln = CIRC*p/100 - 4
    segs += f'<circle class="s" cx="200" cy="200" r="{R}" stroke="{c}" stroke-dasharray="{ln:.1f} {CIRC:.1f}" stroke-dashoffset="{ln:.1f}" data-off="0" transform="rotate({acc*3.6:.2f} 200 200)"/>'
    acc += p
P(f'''<section class="sec z-l" id="series">
<div class="wrap">
  <h2>شش سری ثابت، هر کدام یک کار</h2>
  <p class="lead">با محصول واقعی و صدای مراجعه‌کننده. سهم هر سری از انتشار ماهانه:</p>
  <div class="series">
    <div class="donut"><svg viewBox="0 0 400 400">{segs}</svg><div class="mid"><b>۶</b><span>سری</span></div></div>
    <ol class="slist">{''.join(f'<li style="--c:{c}" data-p="{fa(p)}٪" data-t="{t}"><span class="p">{fa(p)}٪</span><div><h4>{t}</h4><p>{d}</p><small>{f}</small></div></li>' for t,d,f,p,c in series)}</ol>
  </div>
  <div class="smp">
    <figure><img src="img/posts/f1.jpg" alt="" loading="lazy"><figcaption>چرا این، برای من؟</figcaption></figure>
    <figure><img src="img/posts/f3.jpg" alt="" loading="lazy"><figcaption>جعبه رو برگردون</figcaption></figure>
    <figure><img src="img/posts/f10.jpg" alt="" loading="lazy"><figcaption>سؤالی که نزدیک بود نپرسم</figcaption></figure>
  </div>
  <p class="note">«اسم دکتر رو کجا چک کنم؟» دیگر سری ثابت نیست: یک ریلز، به‌اضافهٔ یک هایلایت دائمی در «اصالت و ایمنی». سری «پشت صحنهٔ ساخت» به اجازهٔ فیلم‌برداری در کارخانه نیاز دارد.</p>
</div></section>''')

# DM
wv = ''.join(f'<i style="height:{h}px"></i>' for h in [6,12,18,9,15,20,11,7,14,19,10,6,13,17,8,5,11,15,7,4])
P(f'''<section class="sec z-l dmsec" id="dm">
<div class="wrap split">
  <div class="txt">
    <h2>سه پستی که در دایرکت فرستاده می‌شوند</h2>
    <p class="lead">اینستاگرام «ارسال در دایرکت» را می‌شمارد و پستی را که دست‌به‌دست می‌شود به آدم‌های بیشتری نشان می‌دهد.</p>
    <ol class="fw">
      <li style="--c:{C['silk']}"><h3>«اگه روم نشد بگم، این ویسو یادم بنداز»</h3><p>ویس هشت‌ثانیه‌ای با یک جملهٔ قرض‌گرفتنی: «امروز فقط اومدم سؤال‌هامو بپرسم. می‌خوام خونه بهش فکر کنم.» برای دوستی که می‌ترسد در مطب رودربایستی کند.</p></li>
      <li style="--c:{C['style']}"><h3>«سؤال‌هایی که حق داری در مطب بپرسی»</h3><p>«این سرنگ برای منه و جلوی خودم باز می‌شه؟»، «جعبه‌ش رو می‌شه ببینم؟»، «برچسب اصالتش کجاست؟». مراقبت خواهرانه، بدون متهم کردن کسی.</p></li>
      <li style="--c:{C['smile']}"><h3>«کدومو بذارم پروفایلم؟»</h3><p>دو عکس از یک عصر: یکی با ژست، یکی وسط خنده. ویس دوست: «دومی. صدای خنده‌ت میاد.» گفت‌وگو می‌سازد، حتی بین کسانی که برنامهٔ تزریق ندارند.</p></li>
    </ol>
    <p class="note">معیار هر سه: «ارسال در دایرکت» در آمار خود اینستاگرام؛ نه لایک.</p>
  </div>
  <div class="dev">
    <div class="phone"><div class="scr">{sbar()}
      <div class="dm">
        <div class="dm-h"><span class="ib">{I['back']}</span><span class="av"></span><div><b>سارا</b><small>فعال</small></div></div>
        <div class="dm-b">
          <div class="msg post me"><div class="pu"><i></i>inovosense</div><img src="img/posts/p5.jpg" alt=""></div>
          <div class="msg me">فردا که رفتی، اگه روت نشد بگی، اینو یادت باشه.</div>
          <div class="msg her voice"><span class="pl"></span><span class="wv">{wv}</span><span class="tm">۰:۰۸</span></div>
          <div class="msg her">مرسی. سه‌تا سؤالو هم می‌پرسم.</div>
          <div class="msg post me"><div class="pu"><i></i>inovosense</div><img src="img/posts/p8.jpg" alt=""></div>
          <div class="msg her">جعبه رو هم برمی‌گردونم!</div>
        </div>
        <div class="dm-f"><span>پیام…</span>{I['send']}</div>
      </div>
    </div></div>
  </div>
</div></section>''')

# films
films = [('reel1','لبخندمو دوست دارم','فیلم شروع، ۲۲ ثانیه','img/ai/mirror-916.jpg',
  ['خانه. زنی جلوی آینه موهایش را جمع می‌کند.','خواهرش: «اگه بری مشاوره، اول چی می‌پرسی؟»','رو به آینه تمرین می‌کند: «دکتر، اینووسنس برای من مناسبه؟»','خواهر: «اون چیزی که برام گفتی رو هم بهش بگو.»','در گوشی‌اش می‌نویسد: «لبخندمو دوست دارم. دلم می‌خواد همین‌جوری بمونه.»'],
  'بدون پزشک در قاب. نسخهٔ برنددار فقط پس از استعلام کتبی.'),
 ('reel2','از قنات تا پوست','فیلم برند، ۴۵ ثانیه','img/ai/qanat-corridor-11.jpg',
  ['آب زلال در دل قنات، نور از دهانهٔ چاه.','همان نور، روی خط تای کارت نقشهٔ نور.','دست‌خط روی کارت: «چیزی که برای من مهم است…»','کارت بسته، در کیف مراجعه‌کننده.','پایان: «از عمق تا نور.»'],
  'ماهی یک فیلم از همین سری.'),
 ('reel3','جعبه رو برگردون','اصالت‌سنجی، ۱۵ ثانیه','img/ai/box-flip-916.jpg',
  ['دست، جعبهٔ مشکی را برمی‌گرداند.','نزدیک: برچسب اصالت و شماره.','استعلام در گوشی؛ تیک سبز.','پایان: «قبل از تزریق، جعبه را ببین.»'],
  'پرطرفدارترین الگوی پروفایلو، به زبان ما.')]
BEATIMG = {'reel2': ['img/ai/qanat-corridor-11.jpg','img/ai/card-emboss-43.jpg','img/ai/card-write-916.jpg','img/ai/box-card-tea-45.jpg','img/ai/qanat-corridor-11.jpg']}
side = f'<div class="side">{I["heart"]}{I["cmt"]}{I["send"]}</div>'
P(f'''<section class="sec z-l" id="films">
<div class="wrap">
  <h2>لانچ با جمله‌ای که باید معروف شود</h2>
  <p class="lead">روی هر کاور، صحنه‌های فیلم مثل استوری جلو می‌روند. ویدیوی نهایی که آماده شد، همین‌جا جایش می‌نشیند.</p>
  <div class="reels">{''.join(f"""<figure class="reel"><div class="phone slim"><div class="scr">{sbar(True)}
    <div class="rv" data-key="{k}" data-beats='{H.escape(json.dumps(b, ensure_ascii=False))}' data-imgs='{H.escape(json.dumps(BEATIMG.get(k,[]), ensure_ascii=False))}'><img class="bg" src="{img}" alt=""><div class="shade"></div><div class="bars"></div><div class="beat"></div>{side}<div class="rmeta"><i></i><span>inovosense</span></div></div>
  </div></div><figcaption><h3>{t}</h3><span>{d}</span><p>{n}</p></figcaption></figure>""" for k,t,d,img,b,n in films)}</div>
  <p class="note">همهٔ فیلم‌ها بدون سوزن، بدون صحنهٔ تزریق و بدون پزشک در قاب تبلیغ. کاورها نمونهٔ مفهومی‌اند.</p>
</div></section>''')

# week
days = ['شنبه','یکشنبه','دوشنبه','سه‌شنبه','چهارشنبه','پنجشنبه','جمعه']
plan = [('کاروسل','«چرا این، برای من؟»',C['shine']),('استوری','سؤال هفته',C['smile']),('ریلز','«ویس قبل ویزیت»',C['silk']),('ریلز','«پشت صحنهٔ ساخت» یا «سؤالی که نزدیک بود نپرسم»، یک هفته در میان','#b48a52'),('ریلز','«جعبه رو برگردون»',C['shape']),('ریلز','«ویس قبل ویزیت»',C['silk']),('','استراحت؛ فقط پاسخ دایرکت','transparent')]
P(f'''<section class="sec z-l" id="week">
<div class="wrap">
  <h2>یک هفتهٔ نمونه</h2>
  <ol class="week">{''.join(f'<li style="--c:{c}"><b>{dn}</b><small>{fm}</small><span>{dp}</span></li>' for dn,(fm,dp,c) in zip(days,plan))}</ol>
  <p class="note">هر ماه یک فیلم از سری «از قنات تا پوست». لایو با پزشک فقط پس از تأیید استعلام حقوقی.</p>
</div></section>''')

# ================= CHAPTER 4: EXECUTION =================
P(chapter(4, 'اجرا', 'هویت بصری، لحن، بازیگرها، پیش‌نیازها و نقشهٔ ۹۰ روزه.', 'img/ai/box-card-tea-45.jpg', C['style'], 'l'))
P(f'''<section class="sec z-l" id="plan">
<div class="wrap">
  <h2>روشن، تمیز، با محصول واقعی</h2>
  <div class="dd">
    <div><h3>باید</h3><ul class="plain yes"><li>پس‌زمینهٔ روشن و یک‌رنگ؛ رنگ نوار همان محصول.</li><li>جعبه و سرنگ واقعی، با نور طبیعی از بالا.</li><li>نقش گره‌چینی کم‌رنگ؛ امضای ایرانی برند.</li><li>یک جمله روی هر پست؛ فونت فارسی ثابت.</li><li>۹ پست کنار هم، یک خانواده.</li></ul></div>
    <div><h3>نباید</h3><ul class="plain no"><li>سوزن، خون، کبودی و صحنهٔ تزریق.</li><li>قبل‌وبعد و وعدهٔ نتیجه.</li><li>تصویر تاریک و کدر، طلایی و زرق‌وبرق.</li><li>عکس استوک و چهرهٔ مشهور.</li><li>کلمهٔ «اگزوزوم» به‌عنوان ادعا؛ تخفیف و حراج.</li></ul></div>
  </div>
  <div class="mood"><figure><img src="img/ai/qanat-corridor-11.jpg" alt="" loading="lazy"></figure><figure><img src="img/ai/smile-still-45.jpg" alt="" loading="lazy"></figure><figure><img src="img/ai/box-card-tea-45.jpg" alt="" loading="lazy"></figure><figure><img src="img/ai/abanbar-916.jpg" alt="" loading="lazy"></figure></div>
  <p class="note">مرجع نور و سنگ: تراورتن، نور طبیعی از بالا، آب فیروزه‌ای، سایهٔ نرم. نمونهٔ مفهومی.</p>

  <h2 class="mt2">صدای برند: رک، مهربان، بی‌اغراق</h2>
  <div class="tone">
    <div><h3>لحن</h3><p>کوتاه، روشن و بی‌اغراق. «لازم نیست» گفتن را بلد است. به‌جای وعده، سؤال می‌پرسد.</p></div>
    <div class="pt"><img src="img/ai/portrait-45.jpg" alt="" loading="lazy"><h3>جلوی دوربین</h3><p>مراجعه‌کننده‌ها و همراهانشان، با رضایت‌نامهٔ کتبی. پزشک‌ها فقط در کانال حرفه‌ای و آموزشی اینووکادمی، نه در تبلیغ کالا.</p></div>
    <div><h3>هرگز</h3><p>سلبریتی، اینفلوئنسر با ادعای درمانی، یا هر کسی که پروتکل را آموزش ندیده.</p></div>
  </div>
  <div class="academy"><img src="img/academy1.jpg" alt="" loading="lazy"><img src="img/ai/consult-45.jpg" alt="" loading="lazy"><img src="img/academy3.jpg" alt="" loading="lazy"></div>
  <p class="note">اینووکادمی: آموزش پزشکان و آیین مشاوره، فقط برای کانال حرفه‌ای؛ در تبلیغ پزشک نمی‌آید.</p>

  <h2 class="mt2">پیش از اولین پست تازه</h2>
  <p class="lead">هر کدام انجام شد، تیکش را بزنید.</p>
  <ol class="chk">{''.join(f'<li tabindex="0"><span class="bx"></span><p>{t}</p></li>' for t in [
   '<b>استعلام کتبی و مجوز سیتا</b> برای نام برند، سناریوها، کپشن‌ها و حساب انتشار.',
   '<b>یکی کردن شعار و لوگو:</b> «از عمق تا نور» زیر خود اینووسنس، و بیو بازنویسی شود.',
   '<b>پاک‌سازی:</b> پست «معجزه» و هر ادعای درمانی دیگر بایگانی شود.',
   '<b>فهرست مراکز:</b> شکاف ۳۷ در برابر ۲۰۰ بسته شود؛ با عنوان «شرکت در دورهٔ اینووکادمی» و شهر.',
   '<b>هایلایت ثابت «اصالت و ایمنی»:</b> برچسب، استعلام، پرسش‌های پیش از تزریق.',
   '<b>کارت نقشهٔ نور:</b> طراحی، چاپ و آموزش ۱۲ کلینیک آزمایشی.'])}</ol>

  <h2 class="mt2">نقشهٔ ۹۰ روزه</h2>
  <div class="tl"><div class="rail"><i></i></div><ol class="ph">{''.join(f'<li style="--c:{c}"><span class="d">{d}</span><h3>{v}</h3><ul>{"".join(f"<li>{x}</li>" for x in items)}</ul></li>' for v,d,items,c in [
   ('پاک‌سازی','روز ۱ تا ۱۵',['استعلام کتبی نظام پزشکی','مجوز سیتا','بیو، شعار و لوگو','بایگانی پست‌های پرریسک'],C['shine']),
   ('ساختن آیین','روز ۱۶ تا ۴۵',['طراحی و چاپ کارت','آموزش ۱۲ کلینیک','تولید سه فیلم اصلی','شروع شش سری'],C['silk']),
   ('پخش','روز ۴۶ تا ۷۵',['انتشار هفتگی سری‌ها','کارت در کلینیک‌ها','رویداد اینووکادمی','ناشران سلامت مجاز'],C['smile']),
   ('سنجش','روز ۷۶ تا ۹۰',['مقایسهٔ کلینیک‌های آزمایشی','گزارش معیار اصلی','تصمیم برای گسترش'],C['style'])])}</ol></div>
</div></section>''')

# ================= CHAPTER 5: VISIBILITY =================
P(chapter(5, 'دیده‌شدن', 'صفر تبلیغ متا. بودجه به جایی می‌رود که اعتماد ساخته می‌شود: مطب.', 'img/ai/card-emboss-43.jpg', C['shape'], 'l'))
bud = [('کلینیک‌ها',45,'کیت کارت، آموزش کادر کلینیک، نمایش در مطب',C['shine']),('ناشران سلامت مجاز فارسی',25,'محتوای آموزشی دربارهٔ سؤال‌های پیش از تزریق',C['silk']),
       ('رویداد اینووکادمی',20,'آموزش پزشکان؛ برای کانال حرفه‌ای',C['style']),('سنجش',10,'ثبت معیار اصلی در ۱۲ کلینیک',C['shape'])]
loop = [('پست «چرا این، برای من؟» سؤال را در ذهن می‌کارد.',C['shine']),('بیمار در مطب می‌پرسد: «اینووسنس برای من مناسبه؟»',C['silk']),('پزشک نقشه می‌کشد و کارت می‌دهد.',C['smile']),
        ('برای خواهر یا دوستش ویس می‌فرستد: «فردا که رفتی، این سه‌تا سؤال یادت نره.»',C['style']),('ریلز سه سؤال را در دایرکت برای همان دوست می‌فرستد. اینستاگرام این «ارسال» را می‌شمارد.',C['shape'])]
nodes = ''.join(f'<div class="node" style="--c:{c};top:{50-44*math.cos(2*math.pi*i/5):.1f}%;left:{50-44*math.sin(2*math.pi*i/5):.1f}%">{fa(i+1)}</div>' for i,(t,c) in enumerate(loop))
pairs = ''.join(f'<li><span class="lit">{I["clinic"]}با آیین</span><span>{I["clinic"]}بدون آیین</span></li>' for i in range(6))
P(f'''<section class="sec z-l" id="visibility">
<div class="wrap">
  <h2>بودجه کجا خرج می‌شود</h2>
  <div class="vis">
    <div class="zeroM"><b>صفر</b><p>ریال تبلیغ پولی متا. تبلیغ ادعای درمانی برای عموم ممنوع است، و اعتماد به فیلر از دهان پزشک می‌آید، نه از آگهی.</p></div>
    <div class="bud">{''.join(f'<div class="bd" style="--c:{c};--w:{p}%;--d:{i}"><div class="top"><b>{t}</b><em>{fa(p)}٪</em></div><div class="bar"><i></i></div><p>{d}</p></div>' for i,(t,p,d,c) in enumerate(bud))}</div>
  </div>
  <p class="note">درصدها پیشنهاد اولیه‌اند و با بودجهٔ نهایی کارفرما تنظیم می‌شوند.</p>

  <h2 class="mt2">هر بیمار، بیمار بعدی را می‌آورد</h2>
  <div class="loopw">
    <div class="loop"><svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="none" stroke="currentColor" stroke-opacity=".18" stroke-width=".4" stroke-dasharray="1 1.4"/>
      <circle r="1.4" fill="currentColor"><animateMotion dur="13s" repeatCount="indefinite" path="M50 6 A44 44 0 1 0 50.01 6"/></circle></svg>{nodes}<div class="mid">از مطب به دایرکت،<br>از دایرکت به مطب</div></div>
    <ol class="steps">{''.join(f'<li style="--c:{c}">{t}</li>' for t,c in loop)}</ol>
  </div>

  <h2 class="mt2">آزمایش ۱۲ کلینیکی</h2>
  <div class="pilot">
    <div><ol class="pairs">{pairs}</ol>
      <ul class="plain"><li>شش جفت کلینیک هم‌اندازه و هم‌محله.</li><li>در هر جفت، یکی آیین نقشهٔ نور را اجرا می‌کند و یکی نه.</li><li>منشی یا پزشک، جملهٔ اول بیمار را ثبت می‌کند.</li></ul></div>
    <div class="kpi"><span>معیار اصلی، در هر ۱۰۰ مشاوره</span><b>چند بار بیمار، بی‌آنکه پزشک بگوید، اسم اینووسنس را می‌آورد؟</b>
      <p>معیارهای کمکی: استعلام برچسب اصالت، ذخیرهٔ پست‌ها، ارسال در دایرکت، بازگشت برای جلسهٔ بعد.</p></div>
  </div>
  <div class="two-m">
    <div><span>اثر پیج</span><b>اسم بردن خودجوش، اول مشاوره</b><p>فقط از مراجعه‌کننده‌های تازه، پیش از اینکه کسی در مطب اسم برند را بیاورد. نشان می‌دهد پیج اسم را به مطب رسانده.</p></div>
    <div><span>اثر کارت</span><b>یادآوری اسم، بعد از گرفتن کارت</b><p>فقط میان کسانی که کارت گرفته‌اند: در جلسهٔ بعد، یا با QR اختیاری روی کارت، یک سؤال: «اسم محصولی که دکتر پیشنهاد داد یادتان هست؟». کلینیک برای سنجش با بیمار تماس نمی‌گیرد.</p></div>
    <p class="note">اگر پلهٔ سوم مرحلهٔ صفر (نسخهٔ بی‌نام) اجرا شود، «اثر پیج» طبیعتاً نزدیک صفر است، چون پیج اسمی نمی‌برد؛ در آن حالت فقط «اثر کارت» ملاک است. این از پیش با کارفرما توافق می‌شود.</p>
  </div>
</div></section>''')

# risks + decisions + sources
risks = [('قانون و مجوز','پست بی‌مجوز یا ادعای درمانی','صافی حقوقی پیش از انتشار؛ واژه‌نامهٔ ممنوع'),('پزشک در تبلیغ','تبلیغ تجاری کالا از زبان پزشک تخلف است؛ حذف نام هم کافی نیست','پزشک در محتوای تبلیغاتی نمی‌آید؛ استعلام کتبی پیش از تولید'),
 ('پزشک خارج از پروتکل','نقشهٔ بی‌دقت، تجربهٔ بد','فقط پزشکان آموزش‌دیده در فهرست؛ بازآموزی'),('جعل و تقلب','محصول تقلبی با اسم ما','سری «جعبه رو برگردون»؛ استعلام آسان'),
 ('انتظار بیمار','وعدهٔ ناگفته، نارضایتی','لحن «لازم نیست»؛ بدون قبل‌وبعد'),('کامنت منفی','بحران در صفحه','پاسخ ۲۴ ساعته از تیم پاسخ‌گویی برند؛ نه حذف'),('شباهت به رقبا','دیده شدن مثل کپی','تمایز در آیین و کارت؛ نام نبردن از رقیب'),('عوض شدن برند در مطب','منشی برند دیگری پیشنهاد می‌دهد، مطب همهٔ طبقه‌ها را موجود ندارد، یا پر کردن کارت وقت پزشک را می‌گیرد و کارت ته کشو می‌رود','آموزش پذیرش و دستیار پزشک برای آماده گذاشتن کارت روی پرونده؛ تضمین موجودی و هم‌سویی تجاری ۱۲ کلینیک آزمایشی به‌دست تیم فروش KMT پیش از شروع')]
dec = ['تأیید ایدهٔ «نقشهٔ نور» و جملهٔ «دکتر، اینووسنس برای من مناسبه؟»','شروع استعلام کتبی از مرجع تبلیغات نظام پزشکی (مرحلهٔ صفر).','یکی کردن شعار و لوگو زیر خود اینووسنس، و بایگانی پست‌های پرریسک.','معرفی ۱۲ کلینیک آزمایشی و مسئول هر کدام.','تأیید بودجهٔ ۹۰ روزه و سهم هر بخش.']
qs = ['نقش اینووسنس کنار ژوویدرم و بلوترو در سبد KMT چیست؟', 'برگهٔ رسمی راهنمای محصولات (IFU): دمای نگهداری هر محصول، جنس سرنگ، و برچسب‌های ردیابی داخل جعبه.','اجازهٔ فیلم‌برداری در آزمایشگاه و خط تولید مدیسا آرا گستر، برای سری «پشت صحنهٔ ساخت».',f'رنگ نوار جعبهٔ {en("Shine Exo Plus")} و {en("Mesocell Plus")}، و فایل برداری لوگو.']
src = [('Inovosense','https://www.instagram.com/inovosense/'),('Hydrafacial','https://www.instagram.com/hydrafacial/'),('Restylane USA','https://www.instagram.com/restylaneusa/'),('Profhilo SEA','https://www.instagram.com/profhilo_sea/'),
 ('SkinCeuticals','https://www.instagram.com/skinceuticals/'),('JUVÉDERM','https://www.instagram.com/juvederm/'),('rhode','https://www.instagram.com/rhode/'),('Glossier','https://www.instagram.com/glossier/'),
 ('LANEIGE US','https://www.instagram.com/laneige_us/'),('Anua','https://www.instagram.com/anua_global/'),('SK-II','https://www.instagram.com/skii/'),('Tatcha','https://www.instagram.com/tatcha/'),
 ('Sulwhasoo','https://www.instagram.com/sulwhasoo.official/'),('Beauty of Joseon','https://www.instagram.com/beautyofjoseon_official/'),('medicube','https://www.instagram.com/medicube_global_official/'),('Shiseido','https://www.instagram.com/shiseido/'),
 ('The Ordinary','https://www.instagram.com/theordinary/'),('La Mer','https://www.instagram.com/lamer/'),('Inovosense site','https://inovosense.com/'),('IBSA: Profhilo Structura (2024)','https://www.businesswire.com/news/home/20241001994839/en')]
P(f'''<section class="sec z-l" id="risks">
<div class="wrap">
  <h2>چه چیزی ممکن است خراب شود</h2>
  <div class="tblw"><table class="risk"><thead><tr><th>ریسک</th><th>چه اتفاقی می‌افتد</th><th>راه پیشگیری</th></tr></thead><tbody>
  {''.join(f'<tr class="{"hot" if i in (0,1,7) else ""}"><th>{x}</th><td>{y}</td><td>{z}</td></tr>' for i,(x,y,z) in enumerate(risks))}</tbody></table></div>
</div></section>
<section class="sec z-l" id="next">
<div class="wrap">
  <h2>پنج تصمیم و چهار پاسخ از کارفرما</h2>
  <ol class="chk">{''.join(f'<li tabindex="0"><span class="bx"></span><p>{t}</p></li>' for t in dec)}</ol>
  <h3 class="qh">چهار سؤال از کارفرما</h3>
  <ol class="chk q3c">{''.join(f'<li tabindex="0" class="q"><span class="bx"></span><p>{t}</p></li>' for t in qs)}</ol>
</div></section>
<section class="sec z-l" id="sources">
<div class="wrap">
  <h2>منابع</h2>
  <ul class="srcs">{''.join(f'<li><a href="{u}" target="_blank" rel="noopener"><span class="en">{n}</span><i>{u.replace("https://","").rstrip("/")}</i></a></li>' for n,u in src)}</ul>
  <p class="note">آمار دنبال‌کننده‌ها در آبان ۱۴۰۵ ثبت شده‌اند. پست‌های پیشنهادی طراحی مفهومی‌اند و پیش از انتشار از صافی حقوقی می‌گذرند.</p>
</div></section>
<section class="close z-l"><div class="beam"></div>
<div class="wrap">
  <img src="img/logo_dark.png" alt="INOVO SENSE">
  <p class="bigq"><span class="gm">«</span>دکتر، اینووسنس برای من مناسبه؟<span class="gm">»</span></p>
  <p class="slogan-s">از عمق تا نور</p>
  <div class="bands">{''.join(f'<i style="--c:{C[k]}"></i>' for k in K5)}</div>
</div></section>
<footer class="foot">پروپوزال استراتژی اینستاگرام اینووسنس برای {en('KMT')}، آبان ۱۴۰۵</footer>''')

ALL_POSTS = {**CUR_POSTS, **REF_POSTS, **NEW_POSTS}
HTML = f'''<!DOCTYPE html>
<html lang="fa" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>اینووسنس · از عمق تا نور · پروپوزال اینستاگرام</title>
<meta name="description" content="پروپوزال استراتژی اینستاگرام اینووسنس برای KMT">
<meta name="robots" content="noindex,nofollow">
<link rel="preload" href="fonts/estedad.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/site.css">
</head><body>
{''.join(parts)}
<script>window.IG_POSTS={json.dumps(ALL_POSTS, ensure_ascii=False)};window.BRANDS={json.dumps(BRANDS, ensure_ascii=False)};</script>
<script src="assets/site.js"></script>
</body></html>'''
open('/home/claude/prop/site/index.html', 'w', encoding='utf-8').write(HTML)
print('ok', len(HTML)//1024, 'KB')
