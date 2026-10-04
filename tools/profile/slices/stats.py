from .. import config, frame

def render(ctx: dict) -> tuple[str, str]:
    stats = ctx.get("stats", {})
    cells = [
        ("contributions_ytd", str(stats.get("contributionsTwoYear", 0))),
        ("contributions_all", str(stats.get("contributionsAll", 0))),
        ("streak_current", str(stats.get("streakCurrent", 0))),
        ("streak_longest", str(stats.get("streakLongest", 0))),
        ("repos", str(stats.get("repos", 0))),
        ("member_since", str(stats.get("memberSince", 0))),
    ]
    parts = []
    for i, (label, value) in enumerate(cells):
        x = 40 + (i % 3) * 260
        y = 90 + (i // 3) * 60
        parts.append(f'  <text x="{x}" y="{y}" fill="{config.PALETTE["primary"]}" font-family="{config.MONO_FONT_STACK}" font-size="28" font-weight="700">{value}</text>')
        parts.append(f'  <text x="{x}" y="{y+22}" fill="{config.PALETTE["dim"]}" font-family="{config.MONO_FONT_STACK}" font-size="12">{label}</text>')
    body = "\n".join(parts)
    svg = frame.render_slice("stats.svg", 240, body, title="Stats", desc="Telemetry panel")
    return "stats.svg", svg
