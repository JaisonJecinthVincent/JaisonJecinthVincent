SLICE_W = 880
GRID = 40

PALETTE = {
    "bg": "#05070d",
    "panel": "#080d17",
    "rail": "#12304f",
    "grid": "#0c1826",
    "primary": "#2f81ff",
    "accent": "#00d9ff",
    "text": "#d3e9ff",
    "dim": "#6d8fb5",
    "warn": "#ffb454",
}

class SliceSpec:
    def __init__(self, filename: str, height: int, title: str):
        self.filename = filename
        self.height = height
        self.width = SLICE_W
        self.title = title

slice_registry = [
    SliceSpec("header.svg", 360, "Header"),
    SliceSpec("stats.svg", 440, "Stats"),
    SliceSpec("contribution-city.svg", 680, "City"),
    SliceSpec("stack.svg", 360, "Stack"),
    SliceSpec("footer.svg", 80, "Footer"),
]
