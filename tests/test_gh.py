from datetime import date
from tools.profile.gh import streaks, merge_year_calendars

def test_streak_counts_through_yesterday_when_today_empty():
    days = {
        date(2026, 9, 29): 1,
        date(2026, 9, 30): 1,
        date(2026, 10, 1): 1,
        date(2026, 10, 2): 0,
        date(2026, 10, 3): 1,
    }
    today = date(2026, 10, 4)
    days[today] = 0
    assert streaks(days, today) == (1, 3)

def test_merge_year_calendars_sorts():
    one = [{"date": "2024-01-02", "contributionCount": 1}]
    two = [{"date": "2024-01-01", "contributionCount": 0}]
    result = merge_year_calendars([one, two])
    assert [d["date"] for d in result] == ["2024-01-01", "2024-01-02"]
