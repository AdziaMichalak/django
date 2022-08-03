from django.urls import path
from .views import math, add, sub, mul, div

urlpatterns = [
   path('', math),
   path('add/<int:a>/<b>', add),
   path('sub/<int:a>/<b>', sub),
   path('mul/<int:a>/<b>', mul),
   path('div/<int:a>/<b>', div),
]