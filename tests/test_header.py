from tools.profile.render import build_header

def test_header_svg_contains_whoami():
    svg = build_header()
    assert "whoami" in svg
    assert "Software Engineer" in svg
    assert "Aspiring Systems Engineer" in svg
    assert "Learning Testing, Agentic AI and Open Source" in svg
