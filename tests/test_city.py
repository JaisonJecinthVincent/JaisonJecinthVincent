from tools.profile.slices.city import height_for_count, render

def test_city_height_calculation():
    assert height_for_count(0, 43) == 0
    assert height_for_count(43, 43) > 8
    assert height_for_count(1, 43) > 8

def test_city_skips_zero_contribution_days():
    assert height_for_count(0, 10) == 0
