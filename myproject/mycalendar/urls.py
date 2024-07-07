from django.urls import path
from . import views

app_name = 'mycalendar'

urlpatterns = [
    path('', views.CalendarView.as_view(), name='calendar'),
    path('event-add/', views.EventCreateView.as_view(), name='event_add'),
    path('event-delete/<int:pk>/', views.EventDeleteView.as_view(), name='event_delete'),
    path('event-edit/<int:pk>/', views.EventUpdateView.as_view(), name='event_edit'),  # Nowa ścieżka dla edycji eventu
]
