from django.contrib import admin
from django.urls import path
from greetings.views import greetings, name

urlpatterns = [
   path('', greetings),
   path('<name>/', name)
]