"""Updates the dynamic parts of README.md from data/*.json.

- the alt text of the stats image, so screen readers get today's numbers
- the alt text of the contribution city image
- optionally the latest-articles block between <!-- writing:start --> and <!-- writing:end --> if present

Everything else in the README is left exactly as it is.
"""
import datetime
import html
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
README = HERE.parent.parent / "README.md"
DATA = HERE / "data"


def replace_zone(s: str, tag: str, new_block: str) -> str:
    pattern = re.compile(
        r"<!-- " + re.escape(tag) + r":start -->.*?<!-- " + re.escape(tag) + r":end -->",
        re.DOTALL,
    )
    new_s, n = pattern.subn(
        f"<!-- {tag}:start -->\n{new_block}\n<!-- {tag}:end -->",
        s,
    )
    if n == 0:
        raise RuntimeError(f"No match for marker {tag}:start/end")
    if n > 1:
        raise RuntimeError(f"Multiple matches for marker {tag}:start/end")
    return new_s


def writing_block(articles):
    lines = []
    for i, a in enumerate(articles[:5], 1):
        alt = html.escape(f'{a["title"]} — published {a["published_at"][:10]}, '
                          f'{a["reactions"]} reactions, {a["comments"]} comments', quote=True)
        lines.append(f'<a href="{html.escape(a["url"], quote=True)}"><img src="./assets/writing/post-{i}.svg" '
                     f'width="100%" align="top" alt="{alt}"></a>')
    return "<!-- writing:start -->\n" + "\n".join(lines) + "\n<!-- writing:end -->"


def days(n):
    return f"{n} day" if n == 1 else f"{n} days"


def stats_alt(d):
    since = datetime.date.fromisoformat(d["created_at"][:10])
    langs = sorted(d["languages"].items(), key=lambda kv: -kv[1])[:5]
    parts = [f'{d["stars"]} total stars',
             (f'{d["contributions_year"]} contributions in {d["year"]}, {d["contributions_all"]} all time'
              if "contributions_year" in d else f'{d["commits_year"]} commits in {d["year"]}, {d["commits_all"]} all time'),
             f'{d["prs"]} pull requests ({d["prs_merged"]} merged)',
             f'current streak {days(d["streak_current"])}, longest {days(d["streak_longest"])}',
             f'{d["followers"]} followers', f'{d["forks"]} forks',
             f'member since {since:%B %Y}', f'{d["hackathon_wins"]} hackathon wins']
    text = "Stats: " + "; ".join(parts) + ". Top languages: " + ", ".join(k for k, _ in langs) + "."
    dev = {k: v for k, v in (d.get("dev") or {}).items() if v is not None}
    if dev:
        text += " DEV Community: " + ", ".join(f"{v:,} {k}" for k, v in dev.items()) + "."
    return html.escape(text, quote=True)


def city_alt(calendar):
    total = sum(n for _, n in calendar)
    busiest = max(calendar, key=lambda t: t[1]) if calendar else None
    text = (f"Contribution city: an isometric night skyline with one building per day of the last year. "
            f"{total:,} contributions")
    if busiest and busiest[1]:
        d = datetime.date.fromisoformat(busiest[0])
        text += f", busiest day {d:%B} {d.day} with {busiest[1]}"
    return html.escape(text + ".", quote=True)


def main():
    stats = json.loads((DATA / "stats.json").read_text(encoding="utf-8"))
    s = README.read_text(encoding="utf-8")

    articles_file = DATA / "articles.json"
    if articles_file.exists() and "<!-- writing:start -->" in s:
        articles = json.loads(articles_file.read_text(encoding="utf-8"))
        s = re.sub(r"<!-- writing:start -->.*?<!-- writing:end -->", writing_block(articles), s, flags=re.S)

    s = re.sub(r'(<img src="\./assets/stats\.svg"[^>]*?alt=")[^"]*(")',
               lambda m: m.group(1) + stats_alt(stats) + m.group(2), s)

    cal_file = DATA / "calendar.json"
    if cal_file.exists():
        s = re.sub(r'(<img src="\./assets/(?:contribution-city|city)\.svg"[^>]*?alt=")[^"]*(")',
                   lambda mm: mm.group(1) + city_alt(json.loads(cal_file.read_text(encoding="utf-8"))) + mm.group(2), s)

    README.write_text(s, encoding="utf-8")
    print("README updated")


if __name__ == "__main__":
    main()
