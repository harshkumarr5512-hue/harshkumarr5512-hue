import json
from pathlib import Path
from datetime import datetime

DATA_FILE = Path("assets/contributions.json")
OUTPUT_FILE = Path("graph.svg")

CELL = 12
GAP = 4
LEFT = 45
TOP = 75

LEVELS = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
]

if not DATA_FILE.exists():
    raise FileNotFoundError(
        "assets/contributions.json not found. "
        "Run tools/pull_contributions.py first."
    )

with DATA_FILE.open("r", encoding="utf-8") as file:
    data = json.load(file)

days = data.get("days", [])

if not days:
    raise ValueError("No contribution data found.")

# Group days into weeks
weeks = {}

for day in days:
    date = datetime.strptime(day["date"], "%Y-%m-%d")
    year_week = date.strftime("%Y-%W")

    if year_week not in weeks:
        weeks[year_week] = []

    weeks[year_week].append(
        {
            "date": day["date"],
            "count": int(day.get("count", 0)),
            "level": int(day.get("level", 0)),
            "weekday": date.weekday(),
        }
    )

week_list = list(weeks.values())

WIDTH = LEFT + len(week_list) * (CELL + GAP) + 40
HEIGHT = 255

rectangles = []

for week_index, week in enumerate(week_list):

    for day in week:

        x = LEFT + week_index * (CELL + GAP)

        # Python: Monday = 0
        # GitHub graph style: Sunday at top
        weekday = (day["weekday"] + 1) % 7

        y = TOP + weekday * (CELL + GAP)

        level = max(0, min(day["level"], 4))
        color = LEVELS[level]

        delay = week_index * 0.025

        rectangles.append(
            f'''
            <rect
                x="{x}"
                y="{y}"
                width="{CELL}"
                height="{CELL}"
                rx="3"
                fill="{color}"
                opacity="0">

                <title>{day["date"]}: {day["count"]} contributions</title>

                <animate
                    attributeName="opacity"
                    from="0"
                    to="1"
                    dur="0.25s"
                    begin="{delay:.2f}s"
                    fill="freeze"
                />

            </rect>
            '''
        )

total = data.get(
    "total",
    sum(day["count"] for week in week_list for day in week)
)

current_streak = data.get("current_streak", 0)
longest_streak = data.get("longest_streak", 0)

svg = f'''
<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{WIDTH}"
    height="{HEIGHT}"
    viewBox="0 0 {WIDTH} {HEIGHT}"
>

<style>

.background {{
    fill: #0d1117;
}}

.border {{
    fill: none;
    stroke: #30363d;
    stroke-width: 2;
}}

.heading {{
    font-family: monospace;
    font-size: 19px;
    font-weight: bold;
    fill: #58a6ff;
}}

.label {{
    font-family: monospace;
    font-size: 12px;
    fill: #8b949e;
}}

.stats {{
    font-family: monospace;
    font-size: 13px;
    fill: #c9d1d9;
}}

</style>

<rect
    class="background"
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
    y="40"
    class="heading"
>
$ cat contributions.log
</text>

<text x="15" y="{TOP + 12}" class="label">Sun</text>
<text x="15" y="{TOP + 3 * (CELL + GAP) + 12}" class="label">Wed</text>
<text x="15" y="{TOP + 6 * (CELL + GAP) + 12}" class="label">Sat</text>

{''.join(rectangles)}

<text
    x="35"
    y="220"
    class="stats"
>
Total: {total}  |  Current streak: {current_streak} days  |  Longest streak: {longest_streak} days
</text>

</svg>
'''

OUTPUT_FILE.write_text(svg, encoding="utf-8")

print("graph.svg generated successfully")
