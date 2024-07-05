import calendar
from datetime import date
from .models import Event


def get_month_calendar(year, month):
    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdatescalendar(year, month)
    month_calendar = []

    for week in month_days:
        week_events = []
        for day in week:
            day_events = Event.objects.filter(date=day)
            week_events.append({
                'day': day,
                'events': day_events
            })
        month_calendar.append(week_events)

    return month_calendar
