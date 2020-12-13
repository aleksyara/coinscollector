from django.db import models
from django.urls import reverse

# Create your models here.

DEALS = (
    ('E', 'Exchange'),
    ('S', 'Sale'),
    ('D', 'Donate')
)

class Coin(models.Model):
    material = models.CharField(max_length = 100)
    country = models.CharField(max_length = 100)
    century = models.IntegerField()
    description = models.TextField(max_length = 250)
    
    
    def __str__(self):
        return self.country
    
# method to display a new Coin
    def get_absolute_url(self):
        return reverse('detail', kwargs={'coin_id': self.id})

# Add new Feeding model below Cat model
class Trading(models.Model):
    date = models.DateField('Trading Date')
    deal = models.CharField(
        max_length=1,
        choices=DEALS,
        default=DEALS[0][0] 
        )
    # Create a coin_id as aFK, since a Trading belongs to a Cat
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)

    def __str__(self):
        # Nice method for obtaining the friendly value of a Field.choice
        return f"{self.get_deal_display()} on {self.date}"
    
    class Meta:
        ordering = ['-date'] # most recent dates displayed at the top