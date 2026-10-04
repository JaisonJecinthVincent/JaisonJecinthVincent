import datetime

def merge_year_calendars(years_data: list[list[dict]]) -> list[dict]:
    merged = []
    for year in years_data:
        for day in year:
            merged.append(day)
    merged.sort(key=lambda d: d.get("date", ""))
    return merged

def streaks(days_dict: dict[datetime.date, int], today: datetime.date) -> tuple[int, int]:
    dates = sorted(d for d in days_dict if d <= today)
    longest = run = 0
    for d in dates:
        run = run + 1 if days_dict[d] > 0 else 0
        longest = max(longest, run)
    current = 0
    d = today
    if days_dict.get(d, 0) == 0:
        d -= datetime.timedelta(days=1)
    while days_dict.get(d, 0) > 0:
        current += 1
        d -= datetime.timedelta(days=1)
    return current, longest
