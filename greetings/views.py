from tokenize import Name
from urllib import response
from django.shortcuts import render
from django.http import HttpResponse

def greetings(request):
   return HttpResponse("Hello World!")

def name(request, name):
   return HttpResponse("hello {}!".format(name).title())
