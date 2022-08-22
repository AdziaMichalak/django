from django.contrib import admin
from django.urls import path
from greetings.views import greetings, name, welcome
from django.views.generic import TemplateView


urlpatterns = [
   path('', welcome),
   path('greetings/<name>/', name),
   path('greetings/', greetings),
   path('me/', TemplateView.as_view(template_name="greetings/me.html")),
   path('contact/', TemplateView.as_view(template_name="greetings/contact.html")),
  
]