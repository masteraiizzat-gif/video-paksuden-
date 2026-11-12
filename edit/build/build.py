"""Generates index.html + compositions/*.html for the Pak Su Den story edit.

Run:  python3 build/build.py
Source of truth for the cut is build/timeline.py (EDL). B-roll, graphics and SFX below are
placed on the OUTPUT timeline (seconds). Re-run after changing either file.
"""
import html, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from timeline import build, END_CARD, remap

ROOT = os.path.join(os.path.dirname(__file__), "..")
W, H = 1080, 1920
segs, words, AEND = build()
TOTAL = round(AEND + END_CARD, 3)
GSAP = '<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>'

# ---------------------------------------------------------------- B-roll (output time)
# kind: v = video full-bleed (object-position x%), i = portrait still full-bleed, c = landscape still on a card
BROLL = [
    # HOOK montage
    ("b00", "i", "img/fb_600336398.jpg", 0.00, 1.70, 0, 50),
    ("b01", "v", "video/wa_191412.mp4", 1.70, 3.20, 36.0, 50),
    ("b02", "v", "video/v20s.mp4", 3.20, 4.40, 7.0, 47),
    ("b03", "v", "video/wa_082520.mp4", 4.40, 5.70, 26.0, 50),
    ("b04", "c", "img/IMG_0897.jpg", 5.70, 6.90, 0, 50),
    ("b05", "v", "video/wa_191412.mp4", 6.90, 8.97, 66.0, 50),
    # S1 intro
    ("b06", "i", "img/DT6A1921.jpg", 20.60, 24.01, 0, 50),
    # S2 how it started
    ("b07", "v", "video/wa_082520.mp4", 27.50, 30.00, 0.5, 50),
    ("b08", "i", "img/DT6A1924.jpg", 30.00, 33.11, 0, 50),
    ("b09", "c", "img/hm1jurass.jpg", 40.60, 43.80, 0, 50),
    ("b10", "i", "img/wa_251019.jpg", 43.80, 46.71, 0, 50),
    # S3 international (VO3)
    ("b11", "v", "video/v20s.mp4", 48.40, 51.30, 0.2, 32),
    ("b12", "v", "video/wa_082520.mp4", 51.30, 55.00, 14.0, 50),
    ("b13", "v", "video/v20s.mp4", 55.00, 58.81, 4.0, 45),
    ("b14", "c", "img/IMG_0955.jpg", 58.81, 62.40, 0, 50),
    ("b15", "v", "video/wa_191412.mp4", 62.40, 65.20, 2.0, 50),
    ("b16", "v", "video/v20s.mp4", 65.20, 68.66, 13.0, 52),
    # S4 achievements
    ("b17", "i", "img/wa_251212_b.jpg", 74.71, 77.10, 0, 50),
    ("b18", "i", "img/wa_250126_1829.jpg", 77.10, 79.20, 0, 50),
    ("b19", "c", "img/TANAH-06058.jpg", 79.20, 81.36, 0, 50),
    # S5 sharing / heritage (VO5)
    ("b20", "v", "video/wa_191412.mp4", 83.40, 86.00, 28.0, 50),
    ("b21", "c", "img/DT6A4539.jpg", 86.00, 88.90, 0, 50),
    ("b22", "v", "video/wa_082520.mp4", 88.90, 92.40, 30.0, 50),
    ("b23", "v", "video/v20s.mp4", 92.40, 95.40, 16.0, 36),
    ("b24", "i", "img/wa_250126_1742.jpg", 95.40, 98.30, 0, 50),
    ("b25", "c", "img/DT6A2738.jpg", 98.30, 101.40, 0, 50),
    ("b26", "v", "video/wa_082520.mp4", 104.40, 108.90, 38.5, 50),
    ("b27", "v", "video/wa_191412.mp4", 108.90, 111.46, 46.0, 50),
    # S6 closing
    ("b28", "v", "video/wa_082520.mp4", 116.40, 118.60, 4.0, 50),
    ("b29", "v", "video/v20s.mp4", 118.60, 120.40, 9.0, 56),
    ("b30", "v", "video/wa_191412.mp4", 120.40, 123.40, 68.0, 50),
]

# ---------------------------------------------------------------- SFX (output time, already peak-aligned)
SFX = [
    ("sfx-wh1", "whoosh-short", 1.70 - 0.16, 0.45),
    ("sfx-wh2", "whoosh", 4.40 - 0.16, 0.40),
    ("sfx-wh3", "whoosh-short", 6.90 - 0.16, 0.45),
    ("sfx-riser", "riser", 8.54 - 3.47, 0.35),
    ("sfx-hit1", "impact-bass-1", 8.54 - 0.04, 0.70),
    ("sfx-lt", "whoosh-short", 9.20 - 0.10, 0.35),
    ("sfx-ev", "whoosh-cinematic", 51.40 - 2.50 + 0.35, 0.30),
    ("sfx-pop1", "pop", 70.44 - 0.09, 0.50),
    ("sfx-pop2", "pop", 72.16 - 0.09, 0.50),
    ("sfx-pop3", "pop", 73.16 - 0.09, 0.50),
    ("sfx-war", "sparkle", 103.02, 0.45),
    ("sfx-name", "whoosh", 126.42 - 0.16, 0.35),
    ("sfx-hit2", "impact-bass-2", 131.40 - 1.99, 0.65),
]

BROLL = [(b, k, src, remap(st), remap(en), ms, pos) for (b, k, src, st, en, ms, pos) in BROLL]
SFX = [(i, n, round(remap(st + 0.0001) , 3), v) for (i, n, st, v) in SFX]
SFX_DUR = {'whoosh-short':0.575,'whoosh':0.575,'riser':3.6,'impact-bass-1':2.116,'impact-bass-2':2.592,'pop':0.72,'sparkle':1.802,'whoosh-cinematic':4.2}

# ---------------------------------------------------------------- graphics scenes (host start, duration)
GFX = [
    ("hook-title", 0.0, 8.97),
    ("name-card", 9.05, 6.6),
    ("events-card", 51.30, 7.45),
    ("values", 70.20, 4.45),
    ("warisan", 102.80, 3.70),
    ("name-title", 126.25, 131.11 - 126.25),
]

GFX = [(g, remap(st), round(remap(st + d) - remap(st), 3)) for (g, st, d) in GFX]
GFX_START = {g: st for (g, st, d) in GFX}

EN = [
    "Every success is more than a win — it's an honour to carry Malaysia's name to the world.",
    "My name is Muhammad Abiddin bin Ahmad,",
    "better known as Pak Su Den.",
    "I'm from Malaysia, a practitioner of traditional massage.",
    "It all began with my passion and love for traditional massage.",
    "What began as a passion became a journey that shaped my experience, skills and identity.",
    "This journey took me further — to international massage championships.",
    "Meeting and competing with great therapists from many nations meant so much to me.",
    "Alhamdulillah — through effort, discipline and dedication, I've earned international achievements.",
    "But my journey isn't only about competitions and victories.",
    "I want to keep sharing knowledge, experience and skills with the next generation of therapists.",
    "I believe traditional massage is a heritage to preserve, develop and introduce to the world.",
    "This journey isn't over yet.",
    "I'll keep learning, keep striving, keep carrying Malaysia's name through traditional massage.",
    "I'm Pak Su Den.",
    "This is my journey.",
]
GOLD_WORDS = {"malaysia", "dunia", "penghormatan", "su den", "tradisional", "minat", "identiti",
              "antarabangsa", "negara", "pencapaian", "ilmu", "warisan", "belajar", "berusaha",
              "kejayaan", "generasi"}

COMP_DIR = "compositions"      # where this variant's scene files go
OUT_INDEX = "index.html"       # this variant's root composition
VALUE_HITS = None              # override chip times (output seconds)
MUSIC = None                   # (src, media_start, volume_under_voice, volume_end) or None

COMMON_CSS = """
  :root { --navy:#0b1838; --blue:#1e6fd9; --gold:#f2c14e; --ink:#ffffff; }
  * { margin:0; padding:0; box-sizing:border-box; }
"""

def f(x): return f"{x:.3f}".rstrip("0").rstrip(".") if x else "0"
def esc(s): return html.escape(s, quote=True)

# ================================================================= index.html
def index_html():
    el = []
    z = 1
    # A-roll: each segment a muted <video> inside an untimed framing wrapper + its voice <audio>
    prev_scene = None; k = 0
    for s in segs:
        k = k + 1 if s["scene"] == prev_scene else 0
        prev_scene = s["scene"]
        punch = "punch" if k % 2 == 1 else "wide"
        el.append(f'''      <div class="aroll-frame {punch}">
        <video id="{s['id']}" class="clip aroll" src="assets/video/{s['vsrc']}.mp4" muted playsinline
          data-start="{f(s['start'])}" data-duration="{f(s['dur'])}" data-media-start="{f(s['vin'])}" data-track-index="1"></video>
      </div>''')
    for s in segs:
        el.append(f'''      <audio id="{s['id']}-voice" src="assets/audio/{s['asrc']}.wav" data-start="{f(s['start'])}" data-duration="{f(s['dur'])}"
        data-media-start="{f(s['ain'])}" data-volume="1" data-fade-in="0.03" data-fade-out="0.05" data-track-index="10"></audio>''')
    # B-roll
    for (bid, kind, src, st, en, ms, pos) in BROLL:
        d = round(en - st, 3)
        if kind == "v":
            el.append(f'''      <div class="broll-frame{' toporigin' if 'wa_082520' in src else ''}" id="{bid}-frame">
        <video id="{bid}" class="clip broll" src="assets/{src}" muted playsinline style="object-position:{pos}% 50%"
          data-start="{f(st)}" data-duration="{f(d)}" data-media-start="{f(ms)}" data-track-index="2"></video>
      </div>''')
        elif kind == "i":
            el.append(f'''      <div id="{bid}" class="clip still full" data-start="{f(st)}" data-duration="{f(d)}" data-track-index="2">
        <img id="{bid}-img" src="assets/{src}" alt="" style="object-position:{pos}% 40%" />
      </div>''')
        else:
            el.append(f'''      <div id="{bid}" class="clip still card-bg" data-start="{f(st)}" data-duration="{f(d)}" data-track-index="2">
        <div id="{bid}-card" class="photo-card"><img id="{bid}-img" src="assets/{src}" alt="" /></div>
      </div>''')
    # graphics hosts
    for (gid, st, d) in GFX:
        el.append(f'''      <div id="{gid}" class="gfx" data-composition-id="{gid}" data-composition-src="{COMP_DIR}/{gid}.html"
        data-start="{f(st)}" data-duration="{f(round(d,3))}" data-track-index="4" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>''')
    el.append(f'''      <div id="captions" class="gfx" data-composition-id="captions" data-composition-src="{COMP_DIR}/captions.html"
        data-start="0" data-duration="{f(AEND)}" data-track-index="5" data-track-kind="captions" data-width="{W}" data-height="{H}"></div>''')
    el.append(f'''      <div id="brand" class="gfx" data-composition-id="brand" data-composition-src="{COMP_DIR}/brand.html"
        data-start="0" data-duration="{f(AEND)}" data-track-index="6" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>''')
    el.append(f'''      <div id="endcard" class="gfx" data-composition-id="endcard" data-composition-src="{COMP_DIR}/endcard.html"
        data-start="{f(AEND)}" data-duration="{f(END_CARD)}" data-track-index="7" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>''')
    for (sid, name, st, vol) in SFX:
        dur = min(SFX_DUR[name], TOTAL - st)
        trk = 11 + (SFX.index((sid, name, st, vol)) % 3)
        el.append(f'''      <audio id="{sid}" src="assets/sfx/{name}.mp3" data-start="{f(round(st,3))}" data-duration="{f(round(dur,3))}" data-volume="{vol}" data-track-index="{trk}"></audio>''')

    if MUSIC:
        msrc, mstart, vbed, vend = MUSIC
        # one bed across the whole film; a volume lane lifts it for the hook tail and the end card
        pts = [{"t": 0, "v": vbed}, {"t": round(AEND - 0.4, 3), "v": vbed}, {"t": round(AEND + 0.3, 3), "v": vend}, {"t": round(TOTAL, 3), "v": vend}]
        lane = json.dumps({"version": 1, "lanes": [{"target": "volume", "points": pts}]})
        el.append(f'''      <audio id="music" src="assets/{msrc}" data-start="0" data-duration="{f(TOTAL)}" data-media-start="{f(mstart)}" data-volume="1"
        data-fade-in="0.4" data-fade-out="1.2" data-automation='{lane}' data-track-index="14"></audio>''')
    # root timeline: settle-in moves for B-roll (on wrappers / children, never the timed media)
    tw = []
    for (bid, kind, src, st, en, ms, pos) in BROLL:
        d = en - st
        if kind == "v":
            z = 1.38 if "wa_082520" in src else 1.0
            tw.append(f'tl.fromTo("#{bid}-frame", {{scale:{z+0.12:.2f}}}, {{scale:{z:.2f}, duration:0.55, ease:"expo.out"}}, {st:.3f});')
            tw.append(f'tl.to("#{bid}-frame", {{scale:{z+0.04:.2f}, duration:{max(d-0.55,0.1):.3f}, ease:"none"}}, {st+0.55:.3f});')
        elif kind == "i":
            tw.append(f'tl.fromTo("#{bid}-img", {{scale:1.14}}, {{scale:1.02, duration:{d:.3f}, ease:"power2.out"}}, {st:.3f});')
        else:
            tw.append(f'tl.fromTo("#{bid}-card", {{y:90, rotation:-2.5, scale:0.94, opacity:0}}, {{y:0, rotation:0, scale:1, opacity:1, duration:0.6, ease:"expo.out"}}, {st:.3f});')
            tw.append(f'tl.fromTo("#{bid}-img", {{scale:1.0}}, {{scale:1.07, duration:{d:.3f}, ease:"none"}}, {st:.3f});')
    # hook-end flash on "dunia"
    tw.append('tl.fromTo("#flash", {opacity:0}, {opacity:0.85, duration:0.05, ease:"none"}, 8.54);')
    tw.append('tl.to("#flash", {opacity:0, duration:0.4, ease:"power2.out"}, 8.59);')

    return f'''<!doctype html>
<html lang="ms">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    {GSAP}
    <style>
{COMMON_CSS}
      html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:var(--navy); }}
      #root {{ position:relative; width:100%; height:100%; overflow:hidden; background:var(--navy); }}
      .aroll-frame, .broll-frame {{ position:absolute; inset:0; overflow:hidden; }}
      .aroll-frame {{ z-index:1; }}
      .aroll-frame.punch {{ transform:scale(1.16); transform-origin:50% 26%; }}
      .broll-frame {{ z-index:2; }}
      .broll-frame.toporigin {{ transform-origin:50% 0%; }}
      video.aroll, video.broll {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }}
      .still {{ position:absolute; inset:0; overflow:hidden; z-index:2; }}
      .still.full img {{ width:100%; height:100%; object-fit:cover; display:block; }}
      .still.card-bg {{ background: radial-gradient(120% 70% at 50% 38%, #1d3a7a 0%, #0b1838 62%, #060d22 100%); }}
      .photo-card {{ position:absolute; left:50px; top:330px; width:980px; height:720px; border-radius:28px; overflow:hidden;
                     border:4px solid var(--gold); box-shadow:0 30px 80px rgba(0,0,0,.55); }}
      .photo-card img {{ width:100%; height:100%; object-fit:cover; display:block; }}
      #scrim-top {{ position:absolute; left:0; top:0; width:100%; height:760px; z-index:3; pointer-events:none;
                    background:linear-gradient(180deg, rgba(5,10,28,.70) 0%, rgba(5,10,28,.45) 55%, rgba(5,10,28,0) 100%); }}
      #scrim-bot {{ position:absolute; left:0; top:960px; width:100%; height:960px; z-index:3; pointer-events:none;
                    background:linear-gradient(180deg, rgba(5,10,28,0) 0%, rgba(5,10,28,.58) 45%, rgba(5,10,28,.78) 100%); }}
      #flash {{ position:absolute; inset:0; background:#fff; opacity:0; z-index:20; pointer-events:none; }}
      .gfx {{ position:absolute; inset:0; }}
      #hook-title, #name-card, #events-card, #values, #warisan, #name-title {{ z-index:6; }}
      #captions {{ z-index:8; }}
      #brand {{ z-index:9; }}
      #endcard {{ z-index:12; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{f(TOTAL)}" data-width="{W}" data-height="{H}" data-fps="30">
      <div id="scrim-top" data-layout-ignore></div>
      <div id="scrim-bot" data-layout-ignore></div>
      <div id="flash" data-layout-ignore></div>
{chr(10).join(el)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      {(chr(10)+"      ").join(tw)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''

# ================================================================= scene helper
def scene(cid, dur, css, body, js, extra_head=""):
    return f'''<template>
  {GSAP}
  <style>
{COMMON_CSS}
    #root {{ position:absolute; inset:0; overflow:visible; }}
{css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="{W}" data-height="{H}">
    <div id="{cid}-clip" class="clip" data-start="0" data-duration="{f(round(dur,3))}" style="position:absolute;inset:0">
{body}
    </div>
  </div>
  <script>
    window.__timelines = window.__timelines || {{}};
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
'''

# ================================================================= captions
def captions_html():
    # sentences
    sents = []; cur = []
    for w in words:
        cur.append(w)
        if w["text"].endswith("."): sents.append(cur); cur = []
    if cur: sents.append(cur)
    assert len(sents) == len(EN), (len(sents), len(EN), [" ".join(x["text"] for x in s) for s in sents])
    # groups
    groups = []
    for si, s in enumerate(sents):
        g = []
        for i, w in enumerate(s):
            g.append(w)
            nxt = s[i+1] if i+1 < len(s) else None
            chars = sum(len(x["text"]) + 1 for x in g)
            brk = (nxt is None or w["text"][-1] in ",." or (nxt["start"] - w["end"]) >= 0.3
                   or len(g) >= 4 or chars + len(nxt["text"]) > 21)
            if brk: groups.append((si, g)); g = []
    body = []; js = []
    for gi, (si, g) in enumerate(groups):
        st = max(0.1, g[0]["start"] - 0.06)
        nxt_st = groups[gi+1][1][0]["start"] - 0.06 if gi+1 < len(groups) else AEND
        en = min(max(g[-1]["end"] + 0.35, st + 0.5), nxt_st, AEND - 0.02)
        spans = []
        for wi, w in enumerate(g):
            low = w["text"].lower().strip(".,")
            cls = "w gold" if low in GOLD_WORDS else "w"
            spans.append(f'<span id="cw{gi}-{wi}" class="{cls}">{esc(w["text"])}</span>')
        body.append(f'      <div id="cg{gi}" class="cg">{" ".join(spans)}</div>')
        js.append(f'    tl.fromTo("#cg{gi}", {{opacity:0, y:14}}, {{opacity:1, y:0, duration:0.14, ease:"power3.out"}}, {st:.3f});')
        for wi, w in enumerate(g):
            js.append(f'    tl.fromTo("#cw{gi}-{wi}", {{opacity:0.38}}, {{opacity:1, duration:0.08, ease:"none"}}, {max(st, w["start"]-0.02):.3f});')
        js.append(f'    tl.to("#cg{gi}", {{opacity:0, duration:0.1, ease:"power2.in"}}, {en-0.1:.3f});')
        js.append(f'    tl.set("#cg{gi}", {{visibility:"hidden"}}, {en:.3f});')
    for si, s in enumerate(sents):
        st = max(0.1, s[0]["start"] - 0.06)
        nxt = sents[si+1][0]["start"] - 0.1 if si+1 < len(sents) else AEND
        en = min(s[-1]["end"] + 0.4, nxt, AEND - 0.02)
        body.append(f'      <div id="en{si}" class="en">{esc(EN[si])}</div>')
        js.append(f'    tl.fromTo("#en{si}", {{opacity:0}}, {{opacity:1, duration:0.2, ease:"power2.out"}}, {st:.3f});')
        js.append(f'    tl.to("#en{si}", {{opacity:0, duration:0.15, ease:"power2.in"}}, {en-0.15:.3f});')
        js.append(f'    tl.set("#en{si}", {{visibility:"hidden"}}, {en:.3f});')
    css = """
    .cg { position:absolute; left:0; top:1150px; width:1080px; padding:0 60px; text-align:center; opacity:0;
          font-family:"Montserrat", sans-serif; font-weight:900; font-size:66px; line-height:1.1; color:#fff;
          letter-spacing:-0.01em; text-shadow:0 4px 0 rgba(0,0,0,.55), 0 0 28px rgba(0,0,0,.55); overflow:visible; }
    .cg .w { display:inline-block; }
    .cg .gold { color:var(--gold); }
    .en { position:absolute; left:0; top:1258px; width:1080px; padding:0 90px; text-align:center; opacity:0;
          font-family:"Montserrat", sans-serif; font-weight:500; font-style:italic; font-size:34px; line-height:1.25;
          color:rgba(255,255,255,.88); text-shadow:0 2px 10px rgba(0,0,0,.7); }
"""
    return scene("captions", AEND, css, "\n".join(body), "\n".join(js))

# ================================================================= brand (persistent logo + flag)
FLAG_SVG = '''<svg id="flag-svg" viewBox="0 0 280 140" width="196" height="98" xmlns="http://www.w3.org/2000/svg">
  <rect width="280" height="140" fill="#fff"/>
  ''' + "".join(f'<rect y="{i*10}" width="280" height="10" fill="#CC0001"/>' for i in range(0, 14, 2)) + '''
  <rect width="140" height="80" fill="#010066"/>
  <circle cx="58" cy="40" r="30" fill="#FFCC00"/><circle cx="66" cy="40" r="25.5" fill="#010066"/>
  <polygon fill="#FFCC00" points="''' + " ".join(
    (lambda i: f"{(103 + (24 if i%2==0 else 10.5)*__import__('math').cos(__import__('math').pi*i/14 - __import__('math').pi/2)):.2f},{(40 + (24 if i%2==0 else 10.5)*__import__('math').sin(__import__('math').pi*i/14 - __import__('math').pi/2)):.2f}")(i)
    for i in range(28)) + '''"/>
</svg>'''

def brand_html():
    css = """
    #logo-pill { position:absolute; left:40px; top:176px; height:104px; padding:10px 18px; border-radius:22px;
                 background:rgba(255,255,255,.96); box-shadow:0 10px 30px rgba(0,0,0,.35); display:flex; align-items:center; gap:12px; }
    #logo-pill img { height:84px; width:auto; display:block; }
    #logo-pill .sep { width:2px; height:64px; background:#cfd8e6; }
    #flag-wrap { position:absolute; right:40px; top:180px; border-radius:10px; overflow:hidden;
                 box-shadow:0 10px 30px rgba(0,0,0,.4); transform-origin:0% 50%; }
    #flag-wrap svg { display:block; }
    #flag-gloss { position:absolute; inset:0; background:linear-gradient(100deg, rgba(255,255,255,0) 30%, rgba(255,255,255,.28) 45%, rgba(255,255,255,0) 60%); }
"""
    body = f'''      <div id="logo-pill"><img src="assets/img/logo_psd.png" alt="Pak Su Den" /><div class="sep"></div><img src="assets/img/logo_academy.png" alt="Academy Pak Su Den" /></div>
      <div id="flag-wrap" data-layout-allow-overflow>{FLAG_SVG}<div id="flag-gloss"></div></div>'''
    js = f"""    tl.fromTo("#logo-pill", {{opacity:0, x:-40}}, {{opacity:1, x:0, duration:0.6, ease:"expo.out"}}, 0.15);
    tl.fromTo("#flag-wrap", {{opacity:0, x:40}}, {{opacity:1, x:0, duration:0.6, ease:"expo.out"}}, 0.25);
    // flag: a gloss sweep every 6 s reads as cloth catching light (deterministic, timeline-driven)
    for (let t = 1.0; t < {AEND - 1:.1f}; t += 6) {{
      tl.fromTo("#flag-gloss", {{xPercent:-120}}, {{xPercent:120, duration:1.4, ease:"power1.inOut", immediateRender: t === 1.0}}, t);
    }}
    tl.to(["#logo-pill", "#flag-wrap"], {{opacity:0, duration:0.25, ease:"power2.in"}}, {AEND - 0.3:.3f});"""
    return scene("brand", AEND, css, body, js)

# ================================================================= hook title
def hook_html():
    css = """
    #hk { position:absolute; left:0; top:330px; width:1080px; text-align:center; }
    #hk-kicker { display:inline-block; font-family:"Montserrat",sans-serif; font-weight:800; font-size:30px; letter-spacing:.22em;
                 color:var(--navy); background:var(--gold); padding:10px 22px 9px; border-radius:6px; }
    .hk-line { font-family:"Montserrat",sans-serif; font-weight:900; font-size:96px; line-height:1.0; color:#fff; letter-spacing:-0.02em;
               text-transform:uppercase; text-shadow:0 6px 0 rgba(0,0,0,.45), 0 0 40px rgba(0,0,0,.5); }
    #hk-l1 { margin-top:26px; }
    .hk-line .gold { color:var(--gold); }
    .hk-word { display:inline-block; }
"""
    body = '''      <div id="hk">
        <div id="hk-kicker">WORLD CHAMPION 2025</div>
        <div id="hk-l1" class="hk-line"><span id="hk-w1" class="hk-word">Dari</span> <span id="hk-w2" class="hk-word gold">Malaysia</span></div>
        <div id="hk-l2" class="hk-line"><span id="hk-w3" class="hk-word">ke</span> <span id="hk-w4" class="hk-word">pentas</span> <span id="hk-w5" class="hk-word gold">dunia</span></div>
      </div>'''
    js = """    tl.fromTo("#hk-kicker", {opacity:0, y:-24}, {opacity:1, y:0, duration:0.45, ease:"expo.out"}, 0.05);
    ["#hk-w1","#hk-w2","#hk-w3","#hk-w4"].forEach((s,i) => {
      tl.fromTo(s, {opacity:0, filter:"blur(8px)"}, {opacity:1, filter:"blur(0px)", duration:0.16, ease:"power3.out"}, 0.12 + i*0.08);
    });
    // "dunia" lands with the spoken word + impact
    tl.fromTo("#hk-w5", {opacity:0, scale:1.6, filter:"blur(10px)"}, {opacity:1, scale:1, filter:"blur(0px)", duration:0.32, ease:"expo.out"}, 8.50);
    tl.set("#hk-w5", {opacity:0.0}, 0);
    tl.to("#hk", {opacity:0, y:-30, filter:"blur(6px)", duration:0.22, ease:"power3.in"}, 8.72);"""
    return scene("hook-title", 8.97, css, body, js)

# ================================================================= name card (lower third)
def namecard_html():
    css = """
    #nc { position:absolute; left:64px; top:920px; }
    #nc-kick { display:inline-block; font-family:"Montserrat",sans-serif; font-weight:800; font-size:30px; letter-spacing:.16em;
               color:var(--navy); background:var(--gold); padding:9px 18px 8px; }
    #nc-name { margin-top:14px; font-family:"Montserrat",sans-serif; font-weight:900; font-size:62px; line-height:1; color:#fff;
               text-transform:uppercase; letter-spacing:-0.01em; text-shadow:0 4px 20px rgba(0,0,0,.6); white-space:nowrap; }
    #nc-role { margin-top:12px; font-family:"Montserrat",sans-serif; font-weight:600; font-size:30px; color:rgba(255,255,255,.92);
               text-shadow:0 2px 12px rgba(0,0,0,.7); }
    #nc-line { margin-top:16px; height:6px; width:620px; background:var(--gold); border-radius:3px; transform-origin:0 50%; }
"""
    body = '''      <div id="nc">
        <div id="nc-kick">PAK SU DEN</div>
        <div id="nc-name">Mohd Abiddin Bin Ahmad</div>
        <div id="nc-role">Pengamal Seni Urutan Tradisional · Malaysia</div>
        <div id="nc-line"></div>
      </div>'''
    js = """    tl.fromTo("#nc-kick", {opacity:0, x:-60}, {opacity:1, x:0, duration:0.45, ease:"back.out(1.8)"}, 0.1);
    tl.fromTo("#nc-name", {opacity:0, y:34}, {opacity:1, y:0, duration:0.5, ease:"expo.out"}, 0.25);
    tl.fromTo("#nc-role", {opacity:0}, {opacity:1, duration:0.4, ease:"power2.out"}, 0.5);
    tl.fromTo("#nc-line", {scaleX:0}, {scaleX:1, duration:0.6, ease:"power4.out"}, 0.45);
    tl.to("#nc", {opacity:0, x:-40, duration:0.3, ease:"power2.in"}, 6.2);"""
    return scene("name-card", 6.6, css, body, js)

# ================================================================= events card (S3)
EVENTS = [
    ("SEPANG · MALAYSIA", "SouthEast Asia Massage Championship 2025"),
    ("SINGAPURA", "World Holistic Massage Championship 2025"),
    ("PHUKET · THAILAND", "Newma Asia Massage Championship 2026"),
    ("PENTAS ANTARABANGSA", "Massage Masters Showcase"),
]
def events_html():
    css = """
    #ev { position:absolute; left:60px; top:470px; width:960px; padding:40px 44px 34px; border-radius:30px;
          background:rgba(9,18,44,.84); border:2px solid rgba(242,193,78,.65); box-shadow:0 30px 80px rgba(0,0,0,.5); }
    #ev-title { font-family:"Montserrat",sans-serif; font-weight:900; font-size:50px; color:var(--gold); letter-spacing:.02em; }
    #ev-sub { font-family:"Montserrat",sans-serif; font-weight:600; font-size:28px; color:rgba(255,255,255,.8); margin-top:6px; margin-bottom:22px; }
    .ev-row { display:flex; align-items:center; gap:22px; padding:16px 0; border-top:1px solid rgba(255,255,255,.14); }
    .ev-dot { flex:0 0 22px; height:22px; border-radius:50%; background:var(--gold); box-shadow:0 0 0 6px rgba(242,193,78,.22); }
    .ev-place { font-family:"Montserrat",sans-serif; font-weight:800; font-size:30px; color:#fff; letter-spacing:.06em; }
    .ev-name { font-family:"Montserrat",sans-serif; font-weight:500; font-size:28px; color:rgba(255,255,255,.82); margin-top:4px; }
"""
    rows = "\n".join(f'''        <div id="ev-r{i}" class="ev-row"><div class="ev-dot"></div><div><div class="ev-place">{esc(p)}</div><div class="ev-name">{esc(n)}</div></div></div>'''
                     for i, (p, n) in enumerate(EVENTS))
    body = f'''      <div id="ev">
        <div id="ev-title">PERINGKAT ANTARABANGSA</div>
        <div id="ev-sub">Pertandingan yang disertai Pak Su Den</div>
{rows}
      </div>'''
    js = """    tl.fromTo("#ev", {opacity:0, y:60, scale:0.96}, {opacity:1, y:0, scale:1, duration:0.6, ease:"expo.out"}, 0.1);
    for (let i = 0; i < 4; i++) {
      tl.fromTo("#ev-r"+i, {opacity:0, x:-40}, {opacity:1, x:0, duration:0.45, ease:"expo.out"}, 0.6 + i*0.55);
    }
    tl.to("#ev", {opacity:0, y:-40, duration:0.32, ease:"power3.in"}, 7.05);"""
    return scene("events-card", 7.45, css, body, js)

# ================================================================= values chips (S4)
def values_html():
    base = GFX_START["values"]
    hits = VALUE_HITS if VALUE_HITS else [remap(70.44), remap(72.16), remap(73.16)]
    css = """
    #vals { position:absolute; left:0; top:820px; width:1080px; display:flex; flex-direction:column; align-items:center; gap:18px; }
    .chip { font-family:"Montserrat",sans-serif; font-weight:900; font-size:54px; letter-spacing:.08em; color:var(--navy);
            background:var(--gold); padding:14px 36px 12px; border-radius:16px; box-shadow:0 14px 34px rgba(0,0,0,.4); }
"""
    body = '''      <div id="vals">
        <div id="ch0" class="chip">USAHA</div>
        <div id="ch1" class="chip">DISIPLIN</div>
        <div id="ch2" class="chip">KESUNGGUHAN</div>
      </div>'''
    js = "\n".join(f'    tl.fromTo("#ch{i}", {{opacity:0, scale:0.4}}, {{opacity:1, scale:1, duration:0.42, ease:"back.out(2.2)"}}, {h-base:.3f});' for i, h in enumerate(hits))
    js += '\n    tl.to("#vals", {opacity:0, scale:0.92, duration:0.25, ease:"power2.in"}, 4.15);'
    return scene("values", 4.45, css, body, js)

# ================================================================= warisan title (S5)
def warisan_html():
    css = """
    #wr { position:absolute; left:0; top:300px; width:1080px; text-align:center; }
    #wr-top, #wr-bot { font-family:"Montserrat",sans-serif; font-weight:700; font-size:36px; letter-spacing:.3em; color:#fff;
                       text-shadow:0 2px 14px rgba(0,0,0,.7); }
    #wr-word { font-family:"Playfair Display",serif; font-weight:900; font-size:170px; line-height:1.05; color:var(--gold);
               text-shadow:0 8px 40px rgba(0,0,0,.6); letter-spacing:.02em; }
    .wl { display:inline-block; }
"""
    letters = "".join(f'<span id="wl{i}" class="wl">{c}</span>' for i, c in enumerate("WARISAN"))
    body = f'''      <div id="wr">
        <div id="wr-top">SENI URUTAN TRADISIONAL</div>
        <div id="wr-word">{letters}</div>
        <div id="wr-bot">UNTUK DUNIA</div>
      </div>'''
    js = """    tl.fromTo("#wr-top", {opacity:0}, {opacity:1, duration:0.3, ease:"power2.out"}, 0.05);
    for (let i = 0; i < 7; i++) {
      tl.fromTo("#wl"+i, {opacity:0.0, y:30, filter:"blur(6px)"}, {opacity:1, y:0, filter:"blur(0px)", duration:0.35, ease:"expo.out"}, 0.2 + i*0.06);
    }
    tl.fromTo("#wr-bot", {opacity:0}, {opacity:1, duration:0.3, ease:"power2.out"}, 0.8);
    tl.to("#wr", {opacity:0, filter:"blur(8px)", duration:0.25, ease:"power2.in"}, 3.4);"""
    return scene("warisan", 3.7, css, body, js)

# ================================================================= name title (S6 "Saya Pak Su Den")
def nametitle_html():
    d = dict((g, dd) for (g, st, dd) in GFX)["name-title"]
    css = """
    #nt { position:absolute; left:0; top:330px; width:1080px; text-align:center; }
    #nt-word { font-family:"Playfair Display",serif; font-weight:900; font-size:132px; color:var(--gold); line-height:1;
               text-shadow:0 4px 0 rgba(0,0,0,.5), 0 0 50px rgba(0,0,0,.85); }
    .nl { display:inline-block; }
    #nt-rule { margin:18px auto 0; height:4px; width:520px; background:var(--gold); transform-origin:50% 50%; }
"""
    letters = "".join(f'<span id="nl{i}" class="nl">{"&nbsp;" if c==" " else c}</span>' for i, c in enumerate("Pak Su Den"))
    body = f'''      <div id="nt">
        <div id="nt-word">{letters}</div>
        <div id="nt-rule"></div>
      </div>'''
    js = """    for (let i = 0; i < 10; i++) {
      tl.fromTo("#nl"+i, {opacity:0.25, filter:"blur(4px)"}, {opacity:1, filter:"blur(0px)", duration:0.25, ease:"power2.out"}, 0.15 + i*0.07);
    }
    tl.fromTo("#nt-rule", {scaleX:0}, {scaleX:1, duration:0.7, ease:"power4.out"}, 0.6);
    tl.to("#nt", {opacity:0, duration:0.25, ease:"power2.in"}, %.3f);""" % (d - 0.3)
    return scene("name-title", d, css, body, js)

# ================================================================= end card
def endcard_html():
    css = """
    #ec { position:absolute; inset:0; background: radial-gradient(110%% 60%% at 50%% 42%%, #1d3a7a 0%%, #0b1838 60%%, #050b1d 100%%); }
    #ec-card { position:absolute; left:90px; top:560px; width:900px; padding:40px 40px 34px; border-radius:34px; background:#fff;
               box-shadow:0 40px 90px rgba(0,0,0,.55); text-align:center; }
    #ec-logos { display:flex; align-items:center; justify-content:center; gap:26px; }
    #ec-logos img { height:300px; width:auto; }
    #ec-logos .sep { width:3px; height:220px; background:#d6deea; }
    #ec-tag { margin-top:46px; font-family:"Montserrat",sans-serif; font-weight:900; font-size:54px; color:#fff; letter-spacing:.04em; text-align:center; }
    #ec-sub { margin-top:14px; font-family:"Montserrat",sans-serif; font-weight:600; font-size:32px; color:var(--gold); text-align:center; letter-spacing:.06em; }
    #ec-text { position:absolute; left:0; top:1050px; width:1080px; }
""".replace("%%", "%")
    body = '''      <div id="ec">
        <div id="ec-card"><div id="ec-logos"><img src="assets/img/logo_psd.png" alt="Pak Su Den" /><div class="sep"></div><img src="assets/img/logo_academy.png" alt="Academy Pak Su Den" /></div></div>
        <div id="ec-text">
          <div id="ec-tag">BUKAN SEKADAR RAWATAN</div>
          <div id="ec-sub">PUSAT RAWATAN TERAPI URUTAN TRADISIONAL</div>
        </div>
      </div>'''
    js = """    tl.fromTo("#ec", {opacity:0}, {opacity:1, duration:0.25, ease:"power2.out"}, 0);
    tl.fromTo("#ec-card", {opacity:0, scale:1.35, filter:"blur(10px)"}, {opacity:1, scale:1, filter:"blur(0px)", duration:0.45, ease:"expo.out"}, 0.1);
    tl.fromTo("#ec-tag", {opacity:0, y:30}, {opacity:1, y:0, duration:0.5, ease:"expo.out"}, 0.55);
    tl.fromTo("#ec-sub", {opacity:0}, {opacity:1, duration:0.4, ease:"power2.out"}, 0.8);"""
    return scene("endcard", END_CARD, css, body, js)

def main():
    os.makedirs(os.path.join(ROOT, "compositions"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, COMP_DIR), exist_ok=True)
    out = {
        OUT_INDEX: index_html(),
        f"{COMP_DIR}/captions.html": captions_html(),
        f"{COMP_DIR}/brand.html": brand_html(),
        f"{COMP_DIR}/hook-title.html": hook_html(),
        f"{COMP_DIR}/name-card.html": namecard_html(),
        f"{COMP_DIR}/events-card.html": events_html(),
        f"{COMP_DIR}/values.html": values_html(),
        f"{COMP_DIR}/warisan.html": warisan_html(),
        f"{COMP_DIR}/name-title.html": nametitle_html(),
        f"{COMP_DIR}/endcard.html": endcard_html(),
    }
    for p, s in out.items():
        open(os.path.join(ROOT, p), "w").write(s)
    json.dump(words, open(os.path.join(ROOT, "words.json"), "w"), ensure_ascii=False, indent=0)
    print("total", TOTAL, "segments", len(segs), "words", len(words))

if __name__ == "__main__":
    if os.path.exists(os.path.join(ROOT, "assets", "audio", "music_bed.wav")):
        MUSIC = ("audio/music_bed.wav", 0, 0.13, 0.55)
    main()
