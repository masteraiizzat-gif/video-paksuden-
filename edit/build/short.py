"""Short cut (~58 s) for TikTok / Reels -> ../short/index.html + ../short/compositions/*.html

Run:  python3 build/short.py      (render from ../short: npx hyperframes render -o out.mp4)
Reuses every scene builder in build.py; only the cut, B-roll, graphics, SFX and English lines differ.
Times below are OUTPUT seconds of this cut (no remap).
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import timeline as T

# Story: hook -> who -> international -> achievement -> heritage -> sign-off
EDL = [
    ("hook", "v4", 16.48, "v4_voice", 16.48, 25.70),   # Setiap kejayaan ... di mata dunia.
    ("s1",   "v1",  6.00, "v1_voice",  6.00,  9.66),   # Nama saya Muhammad Abiddin bin Ahmad.
    ("s1",   "v1", 10.08, "v1_voice", 10.08, 14.20),   # Lebih dikenali sebagai Pak Su Den.
    ("s3",   "v3", 14.60, "vo3",      12.95, 22.80),   # Bertemu dan bersaing ... buat saya. (VO3)
    ("s4",   "v4",  2.00, "v4_voice",  2.00,  7.85),   # Alhamdulillah, dengan usaha, disiplin, kesungguhan,
    ("s4",   "v4",  8.18, "v4_voice",  8.18, 15.35),   # saya diberi peluang ... antarabangsa.
    ("s5",   "v5", 19.00, "vo5",      16.95, 30.10),   # Saya percaya ... kepada dunia. (VO5)
    ("s6",   "v6", 20.80, "v6_voice", 20.80, 23.45),   # Inilah perjalanan saya.
]
T.EDL[:] = EDL
import build as B

END_CARD = 3.0
B.END_CARD = END_CARD
B.TOTAL = round(B.AEND + END_CARD, 3)
B.remap = lambda t: t
B.ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "short")   # separate project, assets symlinked
B.COMP_DIR = "compositions"
B.OUT_INDEX = "index.html"

W = {}
for w in B.words:
    W.setdefault(w["text"].lower().strip(".,"), []).append(w["start"])
def at(word, n=0): return W[word][n]

seg = {s["id"]: s for s in B.segs}
S3, S4a, S4b, S5, S6 = (seg[k]["start"] for k in ("a03", "a04", "a05", "a06", "a07"))
AEND = B.AEND

B.BROLL = [
    # hook montage (same as the long cut)
    ("b00", "i", "img/fb_600336398.jpg", 0.00, 1.70, 0, 50),
    ("b01", "v", "video/wa_191412.mp4", 1.70, 3.20, 36.0, 50),
    ("b02", "v", "video/v20s.mp4", 3.20, 4.40, 7.0, 47),
    ("b03", "v", "video/wa_082520.mp4", 4.40, 5.70, 26.0, 50),
    ("b04", "c", "img/IMG_0897.jpg", 5.70, 6.90, 0, 50),
    ("b05", "v", "video/wa_191412.mp4", 6.90, seg["a01"]["start"], 66.0, 50),
    # international (VO3) - all B-roll, the face never shows under the replacement voice
    ("b14", "c", "img/IMG_0955.jpg", S3, S3 + 2.6, 0, 50),
    ("b12", "v", "video/wa_082520.mp4", S3 + 2.6, S3 + 6.2, 14.0, 50),
    ("b13", "v", "video/v20s.mp4", S3 + 6.2, S4a, 4.0, 45),
    # achievements
    ("b17", "i", "img/wa_251212_b.jpg", S4b, S4b + 2.4, 0, 50),
    ("b18", "i", "img/wa_250126_1829.jpg", S4b + 2.4, S4b + 4.7, 0, 50),
    ("b19", "c", "img/TANAH-06058.jpg", S4b + 4.7, S5, 0, 50),
    # heritage (VO5)
    ("b25", "c", "img/DT6A2738.jpg", S5, S5 + 2.7, 0, 50),
    ("b08", "i", "img/DT6A1924.jpg", S5 + 2.7, S5 + 6.5, 0, 50),
    ("b26", "v", "video/wa_082520.mp4", S5 + 6.5, S5 + 9.7, 38.5, 50),
    ("b27", "c", "img/hm1jurass.jpg", S5 + 9.7, S6, 0, 50),
]

hits = [at("usaha"), at("disiplin"), at("kesungguhan")]
B.VALUE_HITS = hits
war = at("warisan")
B.GFX = [
    ("hook-title", 0.0, seg["a01"]["start"]),
    ("name-card", seg["a01"]["start"] + 0.08, 6.6),
    ("events-card", S3 + 2.5, round(S4a - (S3 + 2.5), 3)),
    ("values", round(hits[0] - 0.24, 3), round(min(4.45, S4b - (hits[0] - 0.24)), 3)),
    ("warisan", round(war - 0.22, 3), 3.7),
    ("name-title", S6, round(AEND - S6, 3)),
]
B.GFX_START = {g: st for (g, st, d) in B.GFX}

B.SFX = [
    ("sfx-wh1", "whoosh-short", 1.70 - 0.16, 0.45),
    ("sfx-wh2", "whoosh", 4.40 - 0.16, 0.40),
    ("sfx-wh3", "whoosh-short", 6.90 - 0.16, 0.45),
    ("sfx-riser", "riser", 8.54 - 3.47, 0.35),
    ("sfx-hit1", "impact-bass-1", 8.54 - 0.04, 0.70),
    ("sfx-lt", "whoosh-short", seg["a01"]["start"] + 0.1 - 0.10, 0.35),
    ("sfx-card", "whoosh-short", S3 + 0.05 - 0.16, 0.35),
    ("sfx-ev", "whoosh-cinematic", S3 + 2.6 - 2.50 + 0.35, 0.30),
    ("sfx-pop1", "pop", hits[0] - 0.09, 0.50),
    ("sfx-pop2", "pop", hits[1] - 0.09, 0.50),
    ("sfx-pop3", "pop", hits[2] - 0.09, 0.50),
    ("sfx-war", "sparkle", war, 0.45),
    ("sfx-name", "whoosh", S6 + 0.17 - 0.16, 0.35),
    ("sfx-hit2", "impact-bass-2", AEND + 0.29 - 1.99, 0.65),
]
B.SFX = [(i, n, round(st, 3), v) for (i, n, st, v) in B.SFX]

B.EN = [
    "Every success is more than a win — it's an honour to carry Malaysia's name to the world.",
    "My name is Muhammad Abiddin bin Ahmad,",
    "better known as Pak Su Den.",
    "Meeting and competing with great therapists from many nations meant so much to me.",
    "Alhamdulillah — through effort, discipline and dedication, I've earned international achievements.",
    "I believe traditional massage is a heritage to preserve, develop and introduce to the world.",
    "This is my journey.",
]

MUSIC_FILE = "audio/music_bed.wav"
if os.path.exists(os.path.join(B.ROOT, "assets", MUSIC_FILE)):
    B.MUSIC = (MUSIC_FILE, 0, 0.13, 0.55)

if __name__ == "__main__":
    B.main()
    print("short cut:", B.TOTAL, "s")
