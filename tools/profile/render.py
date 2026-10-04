from pathlib import Path
import json
from tools.profile.slices import about, city, footer, header, matrix, stats

ASSETS_DIR = Path("assets")

def render_asset(path: str, content: str) -> bool:
    try:
        with open(path, "r", encoding="utf-8") as f:
            if f.read() == content:
                return False
    except FileNotFoundError:
        pass
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return True

def main() -> int:
    ctx = {
        "stats": {},
        "calendar": [],
        "languages": {},
    }
    stats_path = Path("tools/profile/data/stats.json")
    if stats_path.exists():
        ctx["stats"] = json.loads(stats_path.read_text(encoding="utf-8"))
    cal_path = Path("tools/profile/data/calendar.json")
    if cal_path.exists():
        ctx["calendar"] = json.loads(cal_path.read_text(encoding="utf-8"))
        # convert "count" to "contributionCount" for city code
        ctx["calendar"] = [
            {**c, "count": c.get("count", c.get("contributionCount", 0))}
            for c in ctx["calendar"]
        ]
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    for module in (header, about, stats, city, matrix, footer):
        filename, svg = module.render(ctx)
        render_asset(str(ASSETS_DIR / filename), svg)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
