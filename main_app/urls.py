from django.urls import path # path function use to define each route.
from . import views

urlpatterns = [
  path('', views.home, name='home'), 
  path('about/', views.about, name='about'), 
]


