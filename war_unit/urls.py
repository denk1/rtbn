from django.urls import path
from . import views

app_name = 'war_unit'

urlpatterns = [
    path('', views.add_or_change_address,
         name='add_war_unit'),
    path('<int:pk>/', views.add_or_change_address,
         name='change_war_unit'),
]