"""logging_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""e
from django.conf.urls import url
from django.contrib import admin
from logging_app import views

urlpatterns = [
    url(r'^users$', views.UsersView.as_view(), name='get_name'),
    url(r'^login$', views.LoginView.as_view(), name='get_name'),
    url(r'^logout$', views.LogoutView.as_view(), name='get_name'),
    url(r'^loginhistory$', views.SessionView.as_view(), name='get_name'),
    url(r'^events$', views.EventsView.as_view(), name='get_name'),
]
