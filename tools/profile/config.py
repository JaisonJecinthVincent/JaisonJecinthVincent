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

MONO_FONT_STACK = (
    'ui-monospace, SFMono-Regular, Menlo, Consolas, '
    '"DejaVu Sans Mono", monospace'
)

class SliceSpec:
    def __init__(self, filename: str, height: int, title: str):
        self.filename = filename
        self.height = height
        self.width = SLICE_W
        self.title = title

slice_registry = [
    SliceSpec("header.svg", 240, "Header"),
    SliceSpec("about.svg", 240, "About"),
    SliceSpec("stats.svg", 240, "Stats"),
    SliceSpec("city.svg", 720, "City"),
    SliceSpec("matrix.svg", 240, "Matrix"),
    SliceSpec("footer.svg", 160, "Footer"),
]
