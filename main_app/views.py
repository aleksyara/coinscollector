from django.shortcuts import render
from .models import Coin #require MODEL additng this line

# Add the Coins class & list and view function below the imports
# class Coin:  # Note that parens are optional if not inheriting from another class
#   def __init__(self, material, country, century, description):
#     self.material = material
#     self.country = country
#     self.century = century
#     self.description = description

# coins = [
#   Coin('silver', 'Russian Impire', 17, 'very rear'),
#   Coin('copper', 'Russian Impire', 18, 'was launched to optimize production costs'),
#   Coin('brass', 'USSR', 20, 'very common coin')
# ]

# Create your views here.

from django.http import HttpResponse

# Define the HOME view
def home(request):
  return HttpResponse('<h1>Do you like coins?</h1>')# simmiluar to res.send

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

