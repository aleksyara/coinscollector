from django.forms import ModelForm
from .models import Trading

class TradingForm(ModelForm):
  class Meta:
    model = Trading
    fields = ['date', 'deal']