from django.shortcuts import render
from .models import Coin #require MODEL additng this line

from django.views.generic.edit import CreateView

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
  return render(request, 'coins/detail.html', {'coin': coin}) #{'coin': coin} - this is what we want to inject to Cats above

