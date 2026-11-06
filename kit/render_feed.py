"""Render every <section class="slide"> of an HTML file to its own PNG.

Usage: python3 render_feed.py page.html out_dir prefix
Writes out_dir/prefix-01.png, -02.png ... and prints each path with any overflow.
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

src, out_dir, prefix = Path(sys.argv[1]).resolve(), Path(sys.argv[2]), sys.argv[3]
out_dir.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    page = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
    page.goto(src.as_uri()); page.wait_for_load_state("networkidle"); page.evaluate("document.fonts.ready")
    slides = page.query_selector_all("section.slide")
    for i, s in enumerate(slides, 1):
        over = s.evaluate("e => e.scrollHeight - e.clientHeight")
        out = out_dir / f"{prefix}-{i:02d}.png"
        s.screenshot(path=str(out))
        print(out, f"overflow={over}px")
    b.close()
