from django.contrib import admin
from django.urls import path
from greetings.views import greetings, name, welcome, me, contact


urlpatterns = [
   path('', welcome),
   path('greetings/<name>/', name),
   path('greetings/', greetings),
   path('me/', me),
   path('contact/', contact),
]