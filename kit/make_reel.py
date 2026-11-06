"""Make a 1080x1920 text Reel from an HTML file of <section class="slide tall"> scenes.

Usage: python3 make_reel.py reel.html out.mp4 [seconds_per_scene ...]
Each scene is held for its duration (default 2.8 s) with a 0.4 s crossfade and a light zoom.
A silent audio track is added (Instagram accepts it; Yasmine can add music in the app if she wants).
"""
import subprocess, sys, tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright

src, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
durs = [float(x) for x in sys.argv[3:]]
tmp = Path(tempfile.mkdtemp())
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.goto(src.as_uri()); pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready")
    scenes = pg.query_selector_all("section.slide")
    files = []
    for i, s in enumerate(scenes):
        f = tmp / f"s{i:02d}.png"; s.screenshot(path=str(f)); files.append(f)
        print(f"scene {i+1} overflow={s.evaluate('e => e.scrollHeight - e.clientHeight')}px")
    b.close()
n = len(files); durs = (durs + [2.8] * n)[:n]; fade = 0.4
inputs, filt = [], []
for i, (f, d) in enumerate(zip(files, durs)):
    inputs += ["-loop", "1", "-t", f"{d + fade}", "-i", str(f)]
    frames = int((d + fade) * 30)
    filt.append(f"[{i}:v]scale=1188:2112,zoompan=z='1+0.04*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps=30,setsar=1[v{i}]")
last, offset = "v0", 0.0
for i in range(1, n):
    offset += durs[i - 1]
    filt.append(f"[{last}][v{i}]xfade=transition=fade:duration={fade}:offset={offset:.2f}[x{i}]"); last = f"x{i}"
total = sum(durs) + fade
cmd = ["ffmpeg", "-y", "-loglevel", "error", *inputs, "-f", "lavfi", "-t", f"{total}", "-i", "anullsrc=r=44100:cl=stereo",
       "-filter_complex", ";".join(filt), "-map", f"[{last}]", "-map", f"{n}:a",
       "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest",
       "-movflags", "+faststart", str(out)]
subprocess.run(cmd, check=True)
print(out, f"{total:.1f}s")
