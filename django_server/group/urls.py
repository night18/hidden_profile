"""
URL configuration for group project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from hidden_profile import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/hidden_profile/create_participant/', views.create_participant),
    path('api/hidden_profile/record_avatar/', views.record_avatar),
    path('api/hidden_profile/pairing/', views.pairing),
    path('api/hidden_profile/candidate_profile_by_turn/', views.candidate_profile_by_turn),
    path('api/hidden_profile/initial_decision/', views.initial_decision),
    path('api/hidden_profile/final_decision/', views.final_decision),
    path('api/hidden_profile/get_bonus/', views.get_bonus)
]
