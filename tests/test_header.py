from tools.profile.slices.header import render

def test_header_svg_contains_whoami():
    name, svg = render({})
    assert "whoami" in svg
    assert "$ " in svg or "whoami" in svg.lower()
