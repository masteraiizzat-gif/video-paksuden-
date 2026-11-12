import sys, json, os, subprocess
import numpy as np
def load(f):
    b=subprocess.run(['ffmpeg','-v','error','-i',f,'-ac','1','-ar','16000','-f','s16le','-'],capture_output=True,check=True).stdout
    return np.frombuffer(b,np.int16).astype(np.float32)/32768.0
from faster_whisper import WhisperModel
m = WhisperModel(sys.argv[1], device="cpu", compute_type="int8")
out = sys.argv[2]
for f in sys.argv[3:]:
    segs, info = m.transcribe(load(f), language="ms", word_timestamps=True, vad_filter=False, beam_size=5)
    res = []
    for s in segs:
        res.append({"start": s.start, "end": s.end, "text": s.text.strip(),
                    "words": [{"s": w.start, "e": w.end, "w": w.word} for w in s.words]})
    name = os.path.splitext(os.path.basename(f))[0]
    json.dump(res, open(f"{out}/{name}.json", "w"), ensure_ascii=False, indent=1)
    with open(f"{out}/{name}.txt", "w") as t:
        for s in res: t.write(f"[{s['start']:6.2f}-{s['end']:6.2f}] {s['text']}\n")
    print("done", name, flush=True)
