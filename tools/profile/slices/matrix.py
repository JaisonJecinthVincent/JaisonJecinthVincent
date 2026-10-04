from .. import config, frame

def render(ctx: dict) -> tuple[str, str]:
    languages = ctx.get("languages", {})
    if not languages:
        languages = {"Python": 40, "TypeScript": 30, "JavaScript": 20, "HTML": 10}
    total = sum(languages.values()) or 1
    parts = []
    x = 40
    for i, (lang, size) in enumerate(languages.items()):
        width = int(760 * size / total)
        color = config.PALETTE["primary"] if i % 2 == 0 else config.PALETTE["accent"]
        parts.append(f'<rect x="{x}" y="120" width="{max(width, 1)}" height="24" fill="{color}"/>')
        parts.append(f'<text x="{x}" y="110" fill="{config.PALETTE["text"]}" font-family="{config.MONO_FONT_STACK}" font-size="12">{lang}</text>')
        x += max(width, 1)
    body = "\n".join(parts)
    svg = frame.render_slice("matrix.svg", 240, body, title="Matrix", desc="Language bar")
    return "matrix.svg", svg
