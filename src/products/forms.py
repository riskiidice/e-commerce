from django import forms
from django.forms.models import modelformset_factory

from .models import Variation

class VariationInventoryForm(forms.ModelForm):
	price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
	inventory = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
	sale_price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

	class Meta():
		model = Variation
		fields = [
			"price",
			"sale_price",
			"inventory"
		]



VariationInventoryFormSet = modelformset_factory(Variation, form=VariationInventoryForm, extra=0)