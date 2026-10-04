import json
import urllib.request
import urllib.error
import datetime
from typing import Any

def graphql(token: str, query: str, variables: dict | None = None) -> dict:
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables or {}}).encode("utf-8"),
        headers={
            "Authorization": f"bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "github-profile-console",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        data = json.loads(response.read())
    if data.get("errors"):
        raise RuntimeError("; ".join(e["message"] for e in data["errors"]))
    return data["data"]

def merge_year_calendars(years_data: list[list[dict]]) -> list[dict]:
    merged = []
    for year in years_data:
        for day in year:
            merged.append(day)
    merged.sort(key=lambda d: d["date"])
    return merged

def streaks(days_dict: dict[datetime.date, int], today: datetime.date) -> tuple[int, int]:
    longest = run = 0
    for day in sorted(days_dict):
        run = run + 1 if days_dict[day] > 0 else 0
        longest = max(longest, run)

    current = 0
    d = today
    if days_dict.get(d, 0) == 0:
        d -= datetime.timedelta(days=1)
    while d in days_dict and days_dict[d] > 0:
        current += 1
        d -= datetime.timedelta(days=1)
    return current, longest

def build_year_alias_query(years: list[int]) -> str:
    parts = []
    for y in years:
        parts.append(
            f'y{y}: contributionsCollection(from: "{y}-01-01T00:00:00Z", to: "{y}-12-31T23:59:59Z") {{\n'
            '  totalCommitContributions\n'
            '  contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }\n'
            '}'
        )
    return "query($login: String!) {\n  user(login: $login) {\n" + "\n".join(parts) + "\n  }\n}"
