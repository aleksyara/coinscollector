from django.urls import path # path function use to define each route.
from . import views

urlpatterns = [
  path('', views.home, name='home'), 
  path('about/', views.about, name='about'), #name used to obtain the correct URL
  path('coins/', views.coins_index, name='index'),  # this route for coins index
  path('coins/<int:coin_id>/', views.coins_detail, name='detail'),
  path('coins/create/', views.CoinCreate.as_view(), name='coins_create'),
  path('coins/<int:pk>/update/', views.CoinUpdate.as_view(), name='coins_update'),
  path('coins/<int:pk>/delete/', views.CoinDelete.as_view(), name='coins_delete'),
  path('coins/<int:coin_id>/add_tradingg/', views.add_trading, name='add_trading'),
  path('coins/<int:ccoin_id>/assoc_expo/<int:expo_id>/', views.assoc_expo, name='assoc_expo'),
  path('expos/', views.ExpoList.as_view(), name='expos_index'),
  path('expos/<int:pk>/', views.ExpoDetail.as_view(), name='expos_detail'),
  path('expos/create/', views.ExpoCreate.as_view(), name='expos_create'),
  path('expos/<int:pk>/update/', views.ExpoUpdate.as_view(), name='expos_update'),
  path('expos/<int:pk>/delete/', views.ExpoDelete.as_view(), name='expos_delete'),
]


