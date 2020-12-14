from django.shortcuts import render, redirect
from .models import Coin, Expo, Photo #require MODEL additng this line
from .forms import TradingForm

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView #Line for Expo Model


#add these 2 lines to work with Photo
import uuid
import boto3

#Determine the correct AWS Service Endpoin. 
S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'catcollectoraleksei'
####################################

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

def add_photo(request, coin_id):
  #<input type="file" name="photo-file"> <-- the client input
  # photo-file will be the "name" attribute on the <input type="file">
  photo_file = request.FILES.get('photo-file', None) # if there is no photo-file, the property will be NONE
  if photo_file:
    s3 = boto3.client('s3') # initiating connection db and aws
    # uuid.uuid4().hex[:6] <- generate an unique "key" for S3 and append photo file name
    # if you want to specify which photo extention you allow, do it here in the key
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):] # ":]" - slicer that cut rest after dot
    # just in case something goes wrong
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      # if I want to delete Photo
      # print(dir(s3)) - if we want to see all available methods
      # s.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=f"media/{item.file.name}")

      # generate url string to save in our db
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      # Create Photo we can assign to cat_id or cat (if you have a cat object)
      Photo.objects.create(url=url, coin_id=coin_id)
    except:
      print('An error occurred uploading file to S3')
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