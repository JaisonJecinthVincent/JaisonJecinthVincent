import tempfile
import os
from tools.profile.gh import merge_year_calendars
from tools.profile.render import render_asset
from tools.profile.readme import replace_zone

def test_pipeline_no_crash_with_empty_calendar():
    assert merge_year_calendars([]) == []
    path = tempfile.mktemp(suffix=".svg")
    try:
        ok = render_asset(path, "<svg></svg>")
        assert ok is True
    finally:
        os.unlink(path)
