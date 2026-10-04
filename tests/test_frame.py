from tools.profile.frame import render_slice

def test_slice_has_role_img():
    svg = render_slice("test.svg", 240, "<text>hi</text>", title="T", desc="D")
    assert 'role="img"' in svg
    assert '<title id="t240">T</title>' in svg
    assert '<desc id="d240">D</desc>' in svg
