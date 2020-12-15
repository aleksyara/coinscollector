from django.shortcuts import render, redirect
from .models import Coin, Expo, Photo #require MODEL additng this line
from .forms import TradingForm

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView #Line for Expo Model

# Add the two imports below
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Import the login_required decorator
from django.contrib.auth.decorators import login_required

# Import the mixin for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin

#add these 2 lines to work with Photo
import uuid
import boto3

#Determine the correct AWS Service Endpoin. 
S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'catcollectoraleksei'
####################################
def signup(request):
  error_message = ""
  if request.method == "POST":
    #then we want to create user form object that includes the data from the browser
    form = UserCreationForm(request.POST) # < - object saved in memory
    if form.is_valid():
      # save user to DB
      user = form.save()
      # login our user (coming from auth)
      login(request, user) # <- this will create session cookie with sent back n forth on every request
      #redirect the user to the index
      return redirect('index') # index is coming frm name urls.py
    else: 
      error_message = 'Invalid sign up - try again'

  # A bad POST or a GET request, we'll render signup.html with an empty form 
  form = UserCreationForm()
  #^ this gives us the Blank Form
  context = {'form': form, 'error_message': error_message} # we injectin form and error to our html page
  return render(request, 'registration/signup.html', context) 


# Create your views here.

class CoinCreate(LoginRequiredMixin, CreateView):
  model = Coin
  fields = ['material', 'country', 'century', 'description']

# Since cats belong to a user, before a new coin can be added to the database, 
# its user is going to have to be assigned to its user attribute that we added to the model earlier.
  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  # form.instance is the cat. We're overriding the CreateView's form_valid method to assign the logged in user,
    # Let the CreateView do its job as usual
    return super().form_valid(form)
    #super() - calling (CreateView)  

# Define the HOME view
def home(request):
  return render(request, 'home.html') 

# Define the ABOUT view
def about(request):
  return render(request, 'about.html')

@login_required
def coins_index(request):
  #add this line below to read all coins in from our model
  # #use our model to get all the cats 
  # coins = Coin.objects.all()
  coins = Coin.objects.filter(user=request.user) #equest.user we have in every single function
  return render(request, 'coins/index.html', { 'coins': coins })

@login_required
def coins_detail(request, coin_id):
  #find the coin that has the id of coin_id
  # it's better use Cat.objects.get rather then .filter
  # cats = Cat.objects.filter(user=request.user)
  coin = Coin.objects.get(id=coin_id)
  #find expos that coin doesn't have and exclude them
  expos_coin_doesnt_join = Expo.objects.exclude(id__in = coin.expos.all().values_list('id'))
  trading_form = TradingForm()
  return render(request, 'coins/detail.html', {
    'coin': coin, 
    'trading_form': trading_form,
    'expos': expos_coin_doesnt_join 
    })

@login_required  
def add_trading(request, coin_id):
  form = TradingForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it has the cat_id assigned
    new_trading = form.save(commit=False) # - every time whe
    new_trading.coin_id = coin_id
    new_trading.save()
  return redirect('detail', coin_id=coin_id)

@login_required
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

@login_required
def assoc_expo(request, coin_id, expo_id):
   # Note that you can pass a toy's id instead of the whole object
  Coin.objects.get(id=coin_id).expos.add(expo_id)
  return redirect('detail', coin_id=coin_id)

@login_required
def unassoc_expo(request, coin_id, expo_id):
  Coin.objects.get(id=coin_id).expos.remove(expo_id)
  return redirect('detail', coin_id=coin_id)

class CoinUpdate(LoginRequiredMixin, UpdateView):
  model = Coin
  fields = '__all__'

class CoinDelete(LoginRequiredMixin, DeleteView):
  model = Coin
  success_url = '/coins/'


class ExpoList(LoginRequiredMixin, ListView):
  model = Expo

class ExpoDetail(LoginRequiredMixin, DetailView):
  model = Expo

class ExpoCreate(LoginRequiredMixin, CreateView):
  model = Expo
  fields = '__all__'

class ExpoUpdate(LoginRequiredMixin, UpdateView):
  model = Expo
  fields = '__all__'

class ExpoDelete(LoginRequiredMixin, DeleteView):
  model = Expo
  success_url = '/expos/'