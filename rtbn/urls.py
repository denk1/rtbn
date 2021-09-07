"""remember_theirs_by_name_pro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',  views.index, name='index'),
    path('data_input/', views.data_input, name='data_input'),
    path('add/', views.add_or_change_person, name='add_person'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('list/', views.persons_listing, name='data_list'),
    path('search/', views.searching, name='search'),
    path('search/<int:type_search>/', views.searching_param, name='search'),
    path("region/", views.region, name="region"),
    path("add_region/", views.add_region, name="add_region"),
    path("distortion/", views.distortion, name="distortion"),
    path("add_distortion/", views.add_distortion, name="add_distortion"),
    path("enlistment_office/", views.enlistment_office, name="enlistment_office"),
    path("add_enlistment_office/", views.add_enlistment_office,
         name="add_enlistment_office"),
    path("address/", include("address.urls", namespace="address")),
    path("war_unit/", include("war_unit.urls", namespace="war_unit")),
    path("cemetery_item/", include("cemetery_item.urls", namespace="cemetery_item")),
    path("calling_team/", views.calling_team, name='calling_team'),
    path("add_calling_team", views.add_calling_team, name='add_calling_team'),
    path("war_operation", views.war_operation, name='war_operation'),
    path("add_war_operation", views.add_war_operation, name="add_war_operation"),
    path("hospital", views.hospital, name='hospital'),
    path("add_hospital", views.add_hospital, name="add_hospital"),
    path("camp", views.camp, name="camp"),
    path("add_camp", views.add_camp, name="add_camp"),
    path("labour_team", views.labour_team, name="labour_team"),
    path("add_labour_team", views.add_labour_team, name="add_labour_team"),
    #path("add/address/", views.test, name='test'),
]
