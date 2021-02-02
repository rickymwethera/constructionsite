from django.urls import path, include
from django.conf.urls import url
from . import views
from django.conf import settings
from django.http import HttpResponseRedirect

urlpatterns=[
    path('',views.home, name = 'home'),
]