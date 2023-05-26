"""
URL configuration for hackaburg_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
import main.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cancel-ride/', views.cancel_ride),
    path('create-ride/', views.create_ride),
    path('login/', views.user_login),
    path('logout/', views.user_logout),
    path('request-join-ride/', views.request_join_ride),
    path('accept-join-request/', views.accept_join_request),
    path('finish-ride/', views.finish_ride),
    path('find-rides/', views.find_rides),
    path('update/', views.update),
    path('get_hubs/', views.get_hubs)
]
