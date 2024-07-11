from django.urls import path
from . import views

app_name = 'progression'

urlpatterns = [
    path('', views.direction_list, name='direction_list'),
    path('direction/<int:direction_id>/', views.subject_list, name='subject_list'),
    path('subject/<int:subject_id>/', views.subject_detail, name='subject_detail'),
    path('element/<int:element_id>/update/', views.update_progress, name='update_progress'),
]
