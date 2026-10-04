from .. import config, frame

def render(ctx: dict) -> tuple[str, str]:
    body = (
        f'  <text x="40" y="80" fill="{config.PALETTE["text"]}" '
        f'font-family="{config.MONO_FONT_STACK}" font-size="14">'
        '$ whoami</text>\n'
        f'  <text x="40" y="120" fill="{config.PALETTE["primary"]}" '
        f'font-family="{config.MONO_FONT_STACK}" font-size="28" font-weight="700" '
        'class="type">jaison@netrunner</text>\n'
        f'  <rect x="40" y="140" width="8" height="20" fill="{config.PALETTE["accent"]}" '
        'class="blink"/>'
    )
    svg = frame.render_slice("header.svg", 240, body, title="Header", desc="Terminal header")
    return "header.svg", svg
