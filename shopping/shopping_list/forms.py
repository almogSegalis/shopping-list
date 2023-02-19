from django import forms
from . import models

class AddItem(forms.ModelForm):
	class Meta:
		model = models.Item
		fields = ['item']