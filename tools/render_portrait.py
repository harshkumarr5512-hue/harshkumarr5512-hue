from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance

INPUT = Path("assets/photo-ready.png")
OUTPUT = Path("portrait.svg")

WIDTH = 66
CHARSET = "@%#*+=-:. "

if not INPUT.exists():
    raise FileNotFoundError(
        "assets/photo-ready.png not found."
    )

img = Image.open(INPUT).convert("L")

# Improve contrast
img = ImageEnhance.Contrast(img).enhance(1.6)

# Crop to square around the main portrait
img = ImageOps.fit(
    img,
    (900, 900),
    method=Image.Resampling.LANCZOS
)

# ASCII characters are taller than they are wide,
# so reduce the image height.
aspect_ratio = img.height / img.width
height = int(WIDTH * aspect_ratio * 0.48)

img = img.resize(
    (WIDTH, height),
    Image.Resampling.LANCZOS
)

pixels = list(img.getdata())

ascii_lines = []

for y in range(height):
    line = ""

    for x in range(WIDTH):
        pixel = pixels[y * WIDTH + x]

        index = int(
            pixel / 255 * (len(CHARSET) - 1)
        )

        line += CHARSET[index]

    ascii_lines.append(line)

FONT_SIZE = 12
LINE_HEIGHT = 13

SVG_WIDTH = 760
SVG_HEIGHT = len(ascii_lines) * LINE_HEIGHT + 100

text_lines = []

for i, line in enumerate(ascii_lines):
    y = 70 + i * LINE_HEIGHT

    safe_line = (
        line.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
    )

    text_lines.append(
        f'<text x="35" y="{y}" class="ascii">{safe_line}</text>'
    )

svg = f'''
<svg
xmlns="http://www.w3.org/2000/svg"
width="{SVG_WIDTH}"
height="{SVG_HEIGHT}"
viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}"
>

<style>

.bg {{
    fill: #0d1117;
}}

.border {{
    fill: none;
    stroke: #30363d;
    stroke-width: 2;
}}

.title {{
    fill: #58a6ff;
    font-family: monospace;
    font-size: 18px;
    font-weight: bold;
}}

.ascii {{
    fill: #39d353;
    font-family: monospace;
    font-size: {FONT_SIZE}px;
    white-space: pre;
}}

</style>

<rect
class="bg"
width="100%"
height="100%"
rx="12"
/>

<rect
class="border"
x="2"
y="2"
width="{SVG_WIDTH - 4}"
height="{SVG_HEIGHT - 4}"
rx="12"
/>

<text
x="35"
y="38"
class="title">
$ render portrait --ascii
</text>

{''.join(text_lines)}

</svg>
'''

OUTPUT.write_text(svg, encoding="utf-8")

print("portrait.svg generated successfully")
