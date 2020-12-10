from django.db import models

# Create your models here.

class Coin(models.Model):
    material = models.CharField(max_length = 100)
    country = models.CharField(max_length = 100)
    century = models.IntegerField()
    description = models.TextField(max_length = 250)
    
    
    def __str__(self):
        return self.country
    
