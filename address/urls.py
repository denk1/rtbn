from django.urls import path
from . import views

app_name = 'address'

urlpatterns = [
    path('', views.add_or_change_address,
         name='add_address'),
    path('<int:pk>/', views.add_or_change_address,
         name='change_address'),
    path('get_full_string/<int:pk>/', views.get_full_str, name='get_full_str'),
]
