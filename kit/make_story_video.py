"""Make a short VIDEO story (1080x1920 mp4) from 2-4 themed story scenes.

Usage: python3 kit/make_story_video.py out.mp4 scene1.html scene2.html [scene3.html ...] [--durs 2.5,2.5,3]
Each scene is a normal story HTML (same skeleton as kit/themes/README.md, same theme for all scenes).
Scenes are held 2.5 s by default with a 0.4 s crossfade and a slow zoom; silent audio track (no voice).
"""
import subprocess, sys, tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright

args = sys.argv[1:]
durs = []
if "--durs" in args:
    i = args.index("--durs"); durs = [float(x) for x in args[i + 1].split(",")]; args = args[:i] + args[i + 2:]
out, scenes = Path(args[0]).resolve(), [Path(a).resolve() for a in args[1:]]
tmp = Path(tempfile.mkdtemp()); files = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    for i, s in enumerate(scenes):
        pg.goto(s.as_uri()); pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready")
        ov = pg.evaluate("() => { const w = document.querySelector('.wrap'); return w ? w.scrollHeight - w.clientHeight : 0; }")
        f = tmp / f"s{i:02d}.png"; pg.screenshot(path=str(f)); files.append(f)
        print(f"scene {i+1} overflow={ov}px")
    b.close()
n = len(files); durs = (durs + [2.5] * n)[:n]; fade = 0.4
inputs, filt = [], []
for i, (f, d) in enumerate(zip(files, durs)):
    inputs += ["-loop", "1", "-t", f"{d + fade}", "-i", str(f)]
    fr = int((d + fade) * 30)
    filt.append(f"[{i}:v]scale=1188:2112,zoompan=z='1+0.035*on/{fr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={fr}:s=1080x1920:fps=30,setsar=1[v{i}]")
last, off = "v0", 0.0
for i in range(1, n):
    off += durs[i - 1]
    filt.append(f"[{last}][v{i}]xfade=transition=fade:duration={fade}:offset={off:.2f}[x{i}]"); last = f"x{i}"
total = sum(durs) + fade
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-f", "lavfi", "-t", f"{total}", "-i", "anullsrc=r=44100:cl=stereo",
                "-filter_complex", ";".join(filt), "-map", f"[{last}]", "-map", f"{n}:a", "-c:v", "libx264", "-preset", "veryfast",
                "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", "-movflags", "+faststart", str(out)], check=True)
print(out, f"{total:.1f}s")
