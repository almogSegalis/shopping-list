from django.shortcuts import render, redirect
from .models import Item
from . import forms

# Create your views here.

def main_shopping_list(request):
	items = Item.objects.all().order_by('date')
	return render(request, 'shopping_list/list.html', { 'items': items })

def add_item(request):
	if request.method == 'POST':
		add = forms.AddItem(request.POST)
		#save item to db
		return redirect('shopping_list:list')
	else:
		add = forms.AddItem()
	return render(request, 'shopping_list/add_item.html', { 'add': add })
