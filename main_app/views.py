from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

# Define the HOME view
def home(request):
  return HttpResponse('<h1>Do you like coins?</h1>')# simmiluar to res.send

# Define the ABOUT view
def about(request):
  return render(request, 'about.html')