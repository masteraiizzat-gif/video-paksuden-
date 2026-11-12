"""Edit decision list: which source ranges play, in what order. Output times are derived."""
import json, os
HERE = os.path.dirname(__file__)
TR = os.path.join(HERE, "..", "..", "transkrip")

# (scene, video_src, video_in, audio_src, audio_in, audio_out)
# For v1/v2/v4/v6 the picture and the voice come from the same file (lip-sync).
# For v3/v5 the original voice is inaudible: picture from v3/v5, voice from the supplied VO.
EDL = [
    ("hook", "v4", 16.48, "v4_voice", 16.48, 25.70),
    ("s1",   "v1",  6.00, "v1_voice",  6.00,  9.66),
    ("s1",   "v1", 10.08, "v1_voice", 10.08, 14.20),
    ("s1",   "v1", 15.06, "v1_voice", 15.06, 22.50),
    ("s2",   "v2",  2.00, "v2_voice",  2.00, 11.10),
    ("s2",   "v2", 17.05, "v2_voice", 17.05, 30.65),
    ("s3",   "v3",  2.40, "vo3",       0.00, 12.10),
    ("s3",   "v3", 14.60, "vo3",      12.95, 22.80),
    ("s4",   "v4",  2.00, "v4_voice",  2.00,  7.85),
    ("s4",   "v4",  8.18, "v4_voice",  8.18, 15.35),
    ("s5",   "v5",  2.00, "vo5",       0.00, 30.10),
    ("s6",   "v6",  2.30, "v6_voice",  2.30,  6.10),
    ("s6",   "v6",  7.20, "v6_voice",  7.20, 17.45),
    ("s6",   "v6", 17.85, "v6_voice", 17.85, 23.45),
]
END_CARD = 3.6

# Baseline the B-roll / graphics / SFX times in build.py were authored against.
# remap() moves an authored time to where the same moment of speech now plays.
BASE = [(16.48, 25.45), (6.00, 9.66), (10.26, 14.20), (15.06, 22.50), (2.00, 11.10), (17.05, 30.65),
        (0.00, 12.10), (12.95, 22.80), (2.00, 8.05), (8.70, 15.35), (0.00, 30.10), (2.30, 6.10),
        (7.20, 17.45), (17.85, 23.45)]

def remap(t):
    bt = 0.0; nt = 0.0
    for (bi, bo), e in zip(BASE, EDL):
        bd = bo - bi; ni, no = e[4], e[5]
        if t < bt + bd or e is EDL[-1]:
            local = t - bt + (bi - ni)
            return round(nt + min(max(local, 0.0), (no - ni) + max(0.0, t - bt - bd)), 3)
        bt += bd; nt += no - ni
    return t

FIX = {"Sudin.": "Su Den.", "Sultan.": "Su Den.", "Abidin": "Abiddin", "peramal": "pengamal",
       "meraik": "meraih", "percapaian": "pencapaian", "dulu.": "dunia.", "Ibu.": "ini.", "berbagai": "pelbagai",
       "Segala": "Segala-galanya", "-galanya": None}
FIX_VO = {"terapi": "terapis"}
# word onsets whisper placed late, checked against the waveform: (audio, whisper start) -> real start
START_FIX = {("v4_voice", 8.84): 8.40}

def words_for(audio_src):
    d = json.load(open(os.path.join(TR, audio_src + ".json")))
    return [w for s in d for w in s["words"]]

def build(edl=None):
    t = 0.0; segs = []; words = []
    for i, (scene, vsrc, vin, asrc, ain, aout) in enumerate(edl or EDL):
        dur = round(aout - ain, 3)
        segs.append(dict(id=f"a{i:02d}", scene=scene, vsrc=vsrc, vin=vin, asrc=asrc, ain=ain, start=round(t, 3), dur=dur))
        for w in words_for(asrc):
            mid = (max(w["s"], ain) + min(w["e"], aout)) / 2
            if w["e"] > ain + 0.08 and w["s"] < aout - 0.08 and ain <= mid <= aout:
                txt = w["w"].strip()
                if txt in FIX:
                    txt = FIX[txt]
                    if txt is None: continue
                if asrc.startswith("vo") and txt.rstrip(".,") in FIX_VO:
                    txt = FIX_VO[txt.rstrip(".,")] + txt[len(txt.rstrip(".,")):]
                ws = START_FIX.get((asrc, round(w["s"], 2)), w["s"])
                if (w["e"] - w["s"]) > 1.6: ws = w["e"] - 0.9
                ws = max(ws, ain + 0.1)
                s = max(ws, ain) - ain + t; e = min(w["e"], aout) - ain + t
                words.append(dict(text=txt, start=round(s, 3), end=round(e, 3), scene=scene))
        t += dur
    return segs, words, round(t, 3)

if __name__ == "__main__":
    segs, words, total = build()
    for s in segs: print(s["id"], s["scene"], s["vsrc"], f"{s['start']:7.2f} +{s['dur']:.2f}")
    print("A-roll total", total, "+ end card", END_CARD)
    cur = None
    for w in words:
        if w["scene"] != cur: cur = w["scene"]; print(f"\n[{cur}]", end=" ")
        print(f"{w['text']}@{w['start']:.2f}", end=" ")
    print()
