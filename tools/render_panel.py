from pathlib import Path
from html import escape

# Harsh Kumar - Living Terminal System Panel

WIDTH = 760
HEIGHT = 330

info = [
    ("USER", "Harsh Kumar"),
    ("ROLE", "BCA Student | Frontend Developer"),
    ("FOCUS", "Web Development"),
    ("STACK", "HTML | CSS | JavaScript | Go"),
    ("NOW", "Learning & Building Projects"),
    ("GITHUB", "harshkumarr5512-hue"),
]

rows = []

y = 105

for key, value in info:
    rows.append(
        f'''
        <text x="45" y="{y}" class="key">{escape(key)}</text>
        <text x="180" y="{y}" class="value">{escape(value)}</text>
        '''
    )
    y += 35

svg = f'''<svg
xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

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
    font-size: 20px;
    font-weight: bold;
}}

.key {{
    fill: #8b949e;
    font-family: monospace;
    font-size: 16px;
}}

.value {{
    fill: #c9d1d9;
    font-family: monospace;
    font-size: 16px;
}}

.cursor {{
    fill: #39d353;
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
width="{WIDTH - 4}"
height="{HEIGHT - 4}"
rx="12"
/>

<text
x="35"
y="50"
class="title">
$ whoami --verbose
</text>

{''.join(rows)}

<rect
class="cursor"
x="45"
y="300"
width="10"
height="18">

<animate
attributeName="opacity"
values="1;0;1"
dur="1s"
repeatCount="indefinite"
/>

</rect>

</svg>
'''

Path("sysinfo.svg").write_text(svg, encoding="utf-8")

print("sysinfo.svg generated successfully")
