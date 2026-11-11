# Story themes — a different look every day

Yasmine asked (11 Nov 2026) for stories that **change style every time**: colours, fonts and layout.
All themes share ONE HTML skeleton; only the stylesheet changes. Examples: `themes/examples/<theme>.png`.

| Theme | Look |
|---|---|
| noir | black, lime accent, uppercase heavy sans (League Spartan) |
| editorial | paper white, Bodoni serif, terracotta accent, magazine rules |
| pop | full hot pink, white heavy type, black CTA |
| forest | deep green, cream text, gold accent, Lora serif |
| cobalt | electric blue with grid, white Jost, yellow accent |
| card | lilac background, big white card, violet accent, Poppins |
| sunset | orange→peach gradient, dark brown, Lora italic punchline |

## Rotation rule
- Look at the **Theme** column of the last rows of LOG.md. Never reuse a theme used in the last 6 stories
  (= go through all 7 before repeating). Pick the one used longest ago.
- Theme `classic` (old cream base.css) is retired from rotation.

## Skeleton (kit/today.html)
```html
<!doctype html><html lang="en"><head><meta charset="utf-8"><link rel="stylesheet" href="themes/THEME.css"></head>
<body><div class="deco d1"></div><div class="deco d2"></div><div class="deco d3"></div>
<div class="wrap">
<div class="label">Label</div>
<!-- ONE of: -->
<div class="main num">+84.6%</div><div class="sub">what the number is</div>
<div class="main text">One short sentence.</div>
<div class="myth">The myth.</div><div class="main text">The reality.</div>
<!-- optional punchline, one <em> word gets the accent colour -->
<div class="take">Punchline with one <em>word</em>.</div>
<!-- CTA only on business-tip stories -->
<div class="cta">DM “STRATEGY”</div>
<div class="footer"><span class="src">Source: Outlet</span><span class="wordmark">Business Begin<i>.</i></span></div>
</div></body></html>
```
Render: `python3 kit/render.py kit/today.html` (overflow must be 0px). Long numbers (6+ characters) in `card`:
add `style="font-size:180px"` to `.main.num` if it touches the card edge — always check the PNG.

## Video stories (Yasmine, 11 Nov 2026: "tu peux mettre même des vidéos")
- Tue / Thu / Sat: the story is a short VIDEO (mp4, 7–10 s): 2–4 scenes, same theme for all scenes, each scene a normal
  story HTML (one short line per scene, max ~8 words). Mon/Wed/Fri/Sun: image story (PNG).
- Build: `python3 kit/make_story_video.py stories/YYYY-MM-DD-<lang>-<slug>.mp4 kit/s1.html kit/s2.html kit/s3.html --durs 2.5,2.5,3.5`
  (overflow 0px each), look at 2 frames with ffmpeg before publishing, then delete the scene HTML files.
- No voice, no faces, no photos. Silent audio track. Example: `themes/examples/video_casestudy_fr.mp4`.

## Case studies (Yasmine, 11 Nov 2026: "tu peux mettre des études de cas")
- New story type "Case study", at least once a week in the type rotation. Two kinds, NEVER invented:
  1. Med Travel Assist (Business Begin's own case study) — only the true facts: built from scratch as our own case study;
     turning point = changing the target audience; leads qualified in FR / EN / AR. CTA allowed (business proof).
  2. A real public case from a reputable source (a clinic, hospital, destination or agency documented in news, an official
     report or a study): what they did → what changed, only stated facts, «Source: <outlet>». NO CTA (sector content).
- Label: EN «Case study · <name>», FR «Étude de cas · <name>». Works well as a 3-scene video (situation → change → lesson).
