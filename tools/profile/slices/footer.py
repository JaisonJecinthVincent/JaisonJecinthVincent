from .. import config, frame

def render(ctx: dict) -> tuple[str, str]:
    body = (
        f'  <text x="40" y="80" fill="{config.PALETTE["text"]}" font-family="{config.MONO_FONT_STACK}" font-size="14">$ exit</text>\n'
        f'  <text x="40" y="110" fill="{config.PALETTE["dim"]}" font-family="{config.MONO_FONT_STACK}" font-size="12">connection to github closed. // EOF</text>'
    )
    svg = frame.render_slice("footer.svg", 160, body, title="Footer", desc="Exit message")
    return "footer.svg", svg
