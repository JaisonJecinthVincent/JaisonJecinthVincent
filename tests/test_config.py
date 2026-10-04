from tools.profile import config

def test_slice_w_is_880():
    assert config.SLICE_W == 880

def test_grid_is_40():
    assert config.GRID == 40

def test_slice_heights_are_multiples_of_grid():
    for s in config.slice_registry:
        assert s.height % config.GRID == 0, s.filename

def test_every_slice_width_is_880():
    for s in config.slice_registry:
        assert s.width == config.SLICE_W
