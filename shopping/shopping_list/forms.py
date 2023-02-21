from django import forms
from . import models

class AddItem(forms.ModelForm):
	class Meta:
		model = models.Item
		fields = ['item']
		labels = {
			'item': '',
		}
		widgets = {
			'item': forms.TextInput(attrs = {
				'class': 'form-control', 
				'placeholder':'Item name', 
				'style':'width:75%'
				})
		}