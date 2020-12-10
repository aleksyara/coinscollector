from django.urls import path # path function use to define each route.
from . import views

urlpatterns = [
  path('', views.home, name='home'), 
  path('about/', views.about, name='about'), #name used to obtain the correct URL
  path('coins/', views.coins_index, name='index'),  # this route for coins index
  path('coins/<int:coin_id>/', views.coins_detail, name='detail')
]


