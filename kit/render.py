"""Render 1080x1920 story HTML files to PNG with headless Chrome.

Usage: python3 render.py story1.html [story2.html ...]
Each file is saved next to its HTML as <name>.png.
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright


def main(paths):
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        page = browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        for raw in paths:
            src = Path(raw).resolve()
            out = src.with_suffix(".png")
            page.goto(src.as_uri())
            page.wait_for_load_state("networkidle")
            page.evaluate("document.fonts.ready")
            # report any content that spills past the safe zone
            overflow = page.evaluate(
                """() => { const w = document.querySelector('.wrap');
                           return w ? w.scrollHeight - w.clientHeight : 0; }"""
            )
            page.screenshot(path=str(out), full_page=False)
            print(f"{out}  overflow={overflow}px")
        browser.close()


if __name__ == "__main__":
    main(sys.argv[1:])
