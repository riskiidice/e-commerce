from django import forms
from .models import Variation

class VariationInventoryForm(forms.ModelForm):
	price = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
   	sale_price = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
	inventory = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))  

	class Meta():
		model = Variation
		fields = [
			"price",
			"sale_price",
			"inventory"
		]

