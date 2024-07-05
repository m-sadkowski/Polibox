from django.urls import path
from . import views

app_name = 'mycalendar'

urlpatterns = [
    path('', views.CalendarView.as_view(), name='calendar'),
    path('event-add/', views.EventCreateView.as_view(), name='event_add'),
]
