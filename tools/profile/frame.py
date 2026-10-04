from . import config

def render_slice(filename: str, height: int, body: str, *, title: str = "", desc: str = "") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{config.SLICE_W}" '
        f'height="{height}" viewBox="0 0 {config.SLICE_W} {height}" '
        f'role="img" aria-labelledby="t{height} d{height}">\n'
        f'  <title id="t{height}">{title}</title>\n'
        f'  <desc id="d{height}">{desc}</desc>\n'
        f'  <rect width="100%" height="100%" fill="{config.PALETTE["bg"]}"/>\n'
        f'  {body}\n'
        f'</svg>'
    )
