from django.shortcuts import render, redirect
from .models import Coin, Expo #require MODEL additng this line
from .forms import TradingForm

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView #Line for Expo Model

# Create your views here.

class CoinCreate(CreateView):
  model = Coin
  fields = '__all__'

# Define the HOME view
def home(request):
  return render(request, 'home.html') 

# Define the ABOUT view
def about(request):
  return render(request, 'about.html')

def coins_index(request):
  #add this line below to read all coins in from our model
  #use our model to get all the cats 
  coins = Coin.objects.all()
  return render(request, 'coins/index.html', { 'coins': coins })

def coins_detail(request, coin_id):
  #find the coin that has the id of coin_id
  # it's better use Cat.objects.get rather then .filter
  coin = Coin.objects.get(id=coin_id)
  #find expos that coin doesn't have and exclude them
  expos_coin_doesnt_join = Expo.objects.exclude(id__in = coin.expos.all().values_list('id'))
  trading_form = TradingForm()
  return render(request, 'coins/detail.html', {
    'coin': coin, 
    'trading_form': trading_form,
    'expos': expos_coin_doesnt_join 
    })
  
def add_trading(request, coin_id):
  form = TradingForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it has the cat_id assigned
    new_trading = form.save(commit=False) # - every time whe
    new_trading.coin_id = coin_id
    new_trading.save()
  return redirect('detail', coin_id=coin_id)

def assoc_expo(request, coin_id, expo_id):
   # Note that you can pass a toy's id instead of the whole object
  Coin.objects.get(id=coin_id).expos.add(expo_id)
  return redirect('detail', coin_id=coin_id)

class CoinUpdate(UpdateView):
  model = Coin
  fields = '__all__'

class CoinDelete(DeleteView):
  model = Coin
  success_url = '/coins/'


class ExpoList(ListView):
  model = Expo

class ExpoDetail(DetailView):
  model = Expo

class ExpoCreate(CreateView):
  model = Expo
  fields = '__all__'

class ExpoUpdate(UpdateView):
  model = Expo
  fields = '__all__'

class ExpoDelete(DeleteView):
  model = Expo
  success_url = '/expos/'