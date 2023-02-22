from django.shortcuts import render, redirect
from .models import Item, Tag
from . import forms
from django.http import HttpResponseRedirect

# Delete an item
def delete_item(request, item_id):
	item = Item.objects.get(pk=item_id)
	item.delete()
	return redirect('shopping_list:list')


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


def main_shopping_list(request, tag_name=None):
	active_tag = None
	items = Item.objects.all().order_by('date')
	tags = Tag.objects.all()
	add = forms.AddItem()

	if tag_name:
		active_tag = Tag.objects.get(name=tag_name)
		items = items.filter(tags__in=[active_tag])

	context = {
		'active_tag': active_tag,
		'tags': tags,
		'items': items,
		'add': add,
	}

	return render(request, 'shopping_list/list.html', context)
