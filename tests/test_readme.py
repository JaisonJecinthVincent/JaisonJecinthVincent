from tools.profile.readme import replace_zone

def test_replace_zone_updates_stats_block():
    readme = "old\n<!-- stats:start -->\n<img src=\"old\">\n<!-- stats:end -->\nafter"
    new = replace_zone(readme, "stats", "<img src=\"new.svg\">")
    assert '<img src="new.svg">' in new
    assert '<img src="old">' not in new

def test_replace_zone_fails_when_marker_missing():
    readme = "<!-- stats:start -->x<!-- stats:end -->"
    try:
        replace_zone(readme, "other", "y")
        assert False
    except RuntimeError as e:
        assert "No match" in str(e)
