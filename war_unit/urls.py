from django.urls import path
from . import views

app_name = 'war_unit'

urlpatterns = [
    path('', views.add_or_change_warunit,
         name='add_war_unit'),
    path('<int:pk>/', views.add_or_change_warunit,
         name='change_war_unit'),
    path('get_war_units/', views.get_war_units,
         name='get_war_units'),
    path('add_war_unit/', views.add_war_unit,
         name='add_war_unit'),
    path('get_full_string/<int:pk>/', views.get_full_str, name='get_full_str'),
]
