import datetime
import json
import os
import sys
from pathlib import Path
from tools.profile import gh

STATS_FILE = Path("tools/profile/data/stats.json")
CALENDAR_FILE = Path("tools/profile/data/calendar.json")

def should_commit_changes(new: dict, old: dict) -> bool:
    return new != old

def main() -> int:
    token = os.environ.get("PROFILE_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        print("No token available", file=sys.stderr)
        return 1

    try:
        viewer = gh.graphql(token, "{ viewer { login } }")
        login = viewer["viewer"]["login"]
    except Exception as ex:
        print(f"GitHub fetch failed: {ex}", file=sys.stderr)
        return 1

    today = datetime.datetime.utcnow()
    calendars = []
    # Try to fetch contributionYears and per-year calendars
    try:
        years_obj = gh.graphql(
            token,
            """query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionYears
    }
  }
}""",
            variables={"login": login},
        )
        years = years_obj["user"]["contributionsCollection"]["contributionYears"]
    except Exception:
        years = [today.year]

    for y in years:
        q = f"""query($login: String!) {{
  user(login: $login) {{
    contributionsCollection(from: "{y}-01-01T00:00:00Z", to: "{y}-12-31T23:59:59Z") {{
      contributionCalendar {{
        totalContributions
        weeks {{
          contributionDays {{
            date
            contributionCount
          }}
        }}
      }}
    }}
  }}
}}"""
        try:
            resp = gh.graphql(token, q, variables={"login": login})
            contrib = resp["user"]["contributionsCollection"]["contributionCalendar"]
            for week in contrib["weeks"]:
                for day in week["contributionDays"]:
                    calendars.append(
                        {"date": day["date"], "count": day["contributionCount"]}
                    )
        except Exception as inner_ex:
            print(f"Year {y} fetch failed: {inner_ex}", file=sys.stderr)

    CALENDAR_FILE.parent.mkdir(parents=True, exist_ok=True)
    CALENDAR_FILE.write_text(json.dumps(calendars, indent=2), encoding="utf-8")
    aggregated = {}
    for d in calendars:
        aggregated[d["date"]] = d["count"]
    stats = {
        "contributionsAll": sum(aggregated.values()),
        "contributionsTwoYear": sum(
            v for k, v in aggregated.items()
            if k.startswith(str(today.year)) or k.startswith(str(today.year - 1))
        ),
        "repos": 0,
        "memberSince": 2024,
    }
    STATS_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATS_FILE.write_text(json.dumps(stats, indent=2), encoding="utf-8")
    return 0

if __name__ == "__main__":
    sys.exit(main())
