from django import forms
from . import models

class AddItem(forms.ModelForm):
	class Meta:
		model = models.Item
		fields = ['name']
		labels = {
			'name': '',
		}
		widgets = {
				'name': forms.TextInput(attrs = {
				'class': 'form-control', 
				'placeholder':"הוסיפי פריט", 
				'list':'datalistOptions',
				'id':'exampleDataList',
				'style':'width:70%; text-align: right',
				})
		}