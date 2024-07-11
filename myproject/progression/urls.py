# progression/urls.py
from django.urls import path
from . import views

app_name = 'progression'

urlpatterns = [
    path('progress/', views.progress, name="progress"),
]
