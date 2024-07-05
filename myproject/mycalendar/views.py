# views.py
from django.views.generic import TemplateView, CreateView
from datetime import date, timedelta
import calendar
from .utils import get_month_calendar
from .models import Event


class CalendarView(TemplateView):
    template_name = 'mycalendar/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = int(self.request.GET.get('year', date.today().year))
        month = int(self.request.GET.get('month', date.today().month))

        # Get the current calendar
        context['calendar'] = get_month_calendar(year, month)
        context['events'] = Event.objects.filter(date__year=year, date__month=month)

        # Calculate previous and next month
        first_day_of_month = date(year, month, 1)
        prev_month_last_day = first_day_of_month - timedelta(days=1)
        next_month_first_day = first_day_of_month + timedelta(days=calendar.monthrange(year, month)[1])

        context['prev_month'] = prev_month_last_day.month
        context['prev_month_year'] = prev_month_last_day.year
        context['next_month'] = next_month_first_day.month
        context['next_month_year'] = next_month_first_day.year

        # Add the name of the current month
        context['current_month_name'] = first_day_of_month.strftime('%B %Y')

        return context


class EventCreateView(CreateView):
    model = Event
    template_name = 'mycalendar/event_form.html'
    fields = ['title', 'description', 'date']
    success_url = '/mycalendar/'  # After creating an event, redirect to the calendar view

