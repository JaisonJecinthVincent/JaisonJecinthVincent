from .. import config, frame

def render(ctx: dict) -> tuple[str, str]:
    body = (
        f'  <text x="40" y="60" fill="{config.PALETTE["dim"]}" font-family="{config.MONO_FONT_STACK}" font-size="12">// about</text>\n'
        f'  <text x="40" y="100" fill="{config.PALETTE["text"]}" font-family="{config.MONO_FONT_STACK}" font-size="14">Final-year CSE student at College of Engineering Guindy, Anna University.</text>\n'
        f'  <text x="40" y="130" fill="{config.PALETTE["text"]}" font-family="{config.MONO_FONT_STACK}" font-size="14">I build AI agents, developer tooling, and browser-based hardware emulators.</text>\n'
        f'  <text x="40" y="160" fill="{config.PALETTE["text"]}" font-family="{config.MONO_FONT_STACK}" font-size="14">Currently learning: agentic AI, compilers, and how much of a browser you can bend.</text>'
    )
    svg = frame.render_slice("about.svg", 240, body, title="About", desc="About panel")
    return "about.svg", svg
