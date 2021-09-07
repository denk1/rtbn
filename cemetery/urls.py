from django.urls import path
from . import views

app_name = 'cemetery'

urlpatterns = [
    path('', views.add_or_change_cemetery_item,
         name='add_cemetery_item'),
    path('<int:pk>/', views.add_or_change_cemetery_item,
         name='change_cemetery_item'),
    path('get_cemetery_items/', views.get_cemetery_items,
         name='get_cemetery_items'),
    path('add_cemetery_item/', views.add_cemetery_item,
         name='add_cemetery_item'),
]