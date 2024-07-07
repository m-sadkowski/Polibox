from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView
from datetime import date, timedelta
import calendar
from .utils import get_month_calendar
from .models import Event
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class CalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'mycalendar/calendar.html'
    login_url = '/users/login/'

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
    success_url = '/mycalendar/'

    def get_initial(self):
        initial = super().get_initial()
        date = self.request.GET.get('date')
        if date:
            initial['date'] = date
        return initial

class EventDeleteView(DeleteView):
    model = Event
    template_name = 'mycalendar/event_confirm_delete.html'
    success_url = reverse_lazy('mycalendar:calendar')

class EventUpdateView(UpdateView):
    model = Event
    template_name = 'mycalendar/event_form.html'  # Szablon formularza edycji eventu
    fields = ['title', 'description', 'date']  # Pola do edycji
    success_url = reverse_lazy('mycalendar:calendar')  # Przekierowanie po zapisaniu zmian

    def get_object(self, queryset=None):
        event_id = self.kwargs['pk']
        return Event.objects.get(pk=event_id)