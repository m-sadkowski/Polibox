from django.urls import path
from . import views

app_name = 'materials'

urlpatterns = [
    path('', views.materials_list, name="list"),
    path('new-material/', views.material_new, name="new-material"),
    path('<slug:slug>/', views.material_page, name="page"),
]