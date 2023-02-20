from django.shortcuts import render, redirect
from .models import Item
from . import forms

# Delete an item
def delete_item(request, item_id):
	item = Item.objects.get(pk=item_id)
	item.delete()
	return redirect('shopping_list:list')

def main_shopping_list(request):
	items = Item.objects.all().order_by('date')
	return render(request, 'shopping_list/list.html', { 'items': items })

def add_item(request):
	if request.method == 'POST':
		add = forms.AddItem(request.POST)
		#save item to db
		add.save()
		return redirect(request.GET.get('next'))
	else:
		add = forms.AddItem()
	return render(request, 'shopping_list/list.html', { 'add': add })
