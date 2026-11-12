"""Generate a music bed locally with MusicGen (facebook/musicgen-small) and loop it to length.

usage: python3 tools/musicgen_bed.py OUT.wav SECONDS_NEEDED "prompt"
Writes OUT.wav (48 kHz stereo, loudness-normalised to -16 LUFS) via ffmpeg crossfade loops.
"""
import subprocess, sys, os, tempfile
import numpy as np, soundfile as sf, torch
from transformers import AutoProcessor, MusicgenForConditionalGeneration

out, need, prompt = sys.argv[1], float(sys.argv[2]), sys.argv[3]
torch.manual_seed(7)
proc = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
inputs = proc(text=[prompt], padding=True, return_tensors="pt")
with torch.no_grad():
    audio = model.generate(**inputs, do_sample=True, guidance_scale=3.0, max_new_tokens=1500)  # ~30 s
sr = model.config.audio_encoder.sampling_rate
seed = audio[0, 0].cpu().numpy().astype(np.float32)
tmp = tempfile.mkdtemp()
seedf = os.path.join(tmp, "seed.wav"); sf.write(seedf, seed, sr)
dur = len(seed) / sr
xf = 3.0
n = max(1, int(np.ceil((need - xf) / (dur - xf))))
args = ["ffmpeg", "-v", "error", "-y"]
for _ in range(n): args += ["-i", seedf]
if n == 1:
    fc = "[0:a]anull[m]"
else:
    fc = ""; prev = "[0:a]"
    for i in range(1, n):
        lab = f"[x{i}]"
        fc += f"{prev}[{i}:a]acrossfade=d={xf}:c1=tri:c2=tri{lab};"; prev = lab
    fc += f"{prev}anull[m]"
fc += f";[m]atrim=0:{need},afade=t=out:st={max(need-2,0)}:d=2,aresample=48000,pan=stereo|c0=c0|c1=c0,loudnorm=I=-16:TP=-2:LRA=9[o]"
subprocess.run(args + ["-filter_complex", fc, "-map", "[o]", "-ar", "48000", out], check=True)
sf.write(out.replace(".wav", "_seed.wav"), seed, sr)
print("wrote", out, f"seed {dur:.1f}s x{n}")
