import json
import requests
from pathlib import Path
from bs4 import BeautifulSoup

USERNAME = "harshkumarr5512-hue"

URL = f"https://github.com/users/{USERNAME}/contributions"

response = requests.get(
    URL,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30
)

response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

days = []

for cell in soup.select("td.ContributionCalendar-day"):

    date = cell.get("data-date")

    if not date:
        continue

    level = int(cell.get("data-level", 0))

    count = 0

    tooltip_id = cell.get("id")

    if tooltip_id:
        tooltip = soup.find(
            "tool-tip",
            {"for": tooltip_id}
        )

        if tooltip:
            text = tooltip.get_text(strip=True)

            first_word = text.split()[0]

            if first_word.isdigit():
                count = int(first_word)

    days.append({
        "date": date,
        "count": count,
        "level": level
    })


def calculate_streaks(days):

    current = 0
    longest = 0
    running = 0

    for day in days:

        if day["count"] > 0:
            running += 1
            longest = max(longest, running)
        else:
            running = 0

    for day in reversed(days):

        if day["count"] > 0:
            current += 1
        else:
            break

    return current, longest


current_streak, longest_streak = calculate_streaks(days)

total = sum(day["count"] for day in days)

data = {
    "username": USERNAME,
    "total": total,
    "current_streak": current_streak,
    "longest_streak": longest_streak,
    "days": days
}

Path("assets").mkdir(exist_ok=True)

Path("assets/contributions.json").write_text(
    json.dumps(data, indent=2),
    encoding="utf-8"
)

print(f"Downloaded {len(days)} contribution days.")
print("assets/contributions.json generated successfully.")
