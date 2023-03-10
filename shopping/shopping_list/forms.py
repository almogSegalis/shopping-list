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
				'id':'dataList',
				'style':'width: 90%;',
				})
		}