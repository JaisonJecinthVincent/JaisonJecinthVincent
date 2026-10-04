import tempfile
import os
from tools.profile.render import render_asset

def test_render_does_not_overwrite_same_bytes():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".svg", delete=False) as f:
        f.write("<svg>existing</svg>")
        path = f.name
    try:
        ok = render_asset(path, "<svg>existing</svg>")
        assert ok is False
    finally:
        os.unlink(path)

def test_render_writes_new_when_different():
    path = "test.svg"
    try:
        ok = render_asset(path, "<svg>new</svg>")
        assert ok is True
        assert open(path).read() == "<svg>new</svg>"
    finally:
        os.unlink(path)
