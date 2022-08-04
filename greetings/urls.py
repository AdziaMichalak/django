from django.contrib import admin
from django.urls import path
from greetings.views import greetings, name

urlpatterns = [
   path('admin/', admin.site.urls),
   path('', greetings),
   path('<name>/', name)
]