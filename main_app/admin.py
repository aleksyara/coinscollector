from django.contrib import admin

from .models import Coin, Trading, Expo #in order to see Cat model in the Admin portal

# Register your models here
admin.site.register(Coin)
admin.site.register(Trading)
admin.site.register(Expo)