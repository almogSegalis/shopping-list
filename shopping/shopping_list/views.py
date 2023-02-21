from django.shortcuts import render, redirect
from .models import Item
from . import forms
from django.http import HttpResponseRedirect

# Delete an item
def delete_item(request, item_id):
	item = Item.objects.get(pk=item_id)
	item.delete()
	return redirect('shopping_list:list')

def main_shopping_list(request):
	items = Item.objects.all().order_by('date')
	add = forms.AddItem()
	return render(request, 'shopping_list/list.html', { 'items': items , 'add': add })

def add_item(request):
	if request.method == 'POST':
		add = forms.AddItem(request.POST)
		#save item to db
		if add.is_valid():
			if not Item.objects.filter(name=request.POST['name']).exists():
				add.save()
		return redirect('shopping_list:list')
	else:
		add = forms.AddItem()
	return render(request, 'shopping_list/list.html', { 'add': add })
