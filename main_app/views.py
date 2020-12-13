from django.shortcuts import render, redirect
from .models import Coin #require MODEL additng this line
from .forms import TradingForm

from django.views.generic.edit import CreateView, UpdateView, DeleteView

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

  trading_form = TradingForm()
  return render(request, 'coins/detail.html', {
    'coin': coin, 'trading_form': trading_form 
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

class CoinUpdate(UpdateView):
  model = Coin
  fields = '__all__'

class CoinDelete(DeleteView):
  model = Coin
  success_url = '/coins/'