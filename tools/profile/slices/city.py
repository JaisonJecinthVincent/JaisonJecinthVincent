import math
import random
from tools.profile import config, frame

def height_for_count(count: int, c_max: int) -> int:
    if count == 0:
        return 0
    if c_max == 0:
        return 8
    return int(8 + 110 * math.sqrt(count / c_max))

def render(ctx: dict) -> tuple[str, str]:
    calendar = ctx.get("calendar", [])
    busiest = max((d.get("count", 0) for d in calendar), default=0)
    buildings = []
    for i, day in enumerate(calendar):
        h = height_for_count(day.get("count", 0), busiest)
        if h == 0:
            continue
        x = 60 + i * 12
        y = 700 - h
        w = 10
        half_w = w / 2
        sky_h = half_w
        color = config.PALETTE["primary"]
        roof = config.PALETTE["accent"]
        # front face
        buildings.append(
            f'<polygon points="{x},{y} {x + half_w},{y + half_w} {x + half_w},{y + h} {x},{y + h}" '
            f'fill="{color}" opacity="0.8"/>'
        )
        # side face
        buildings.append(
            f'<polygon points="{x + half_w},{y + half_w} {x + w},{y} {x + w},{y + h} {x + half_w},{y + h}" '
            f'fill="{config.PALETTE["dim"]}" opacity="0.6"/>'
        )
        # roof
        buildings.append(
            f'<polygon points="{x},{y} {x + half_w},{y - half_w} {x + w},{y}" '
            f'fill="{roof}" opacity="0.9"/>'
        )
    body = "\n".join(buildings)
    svg = frame.render_slice("city.svg", 720, body, title="City", desc="Contribution city")
    return "city.svg", svg
