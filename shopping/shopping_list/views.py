from django.shortcuts import render, redirect
from .models import Item, Tag
from . import forms

from django.http import JsonResponse
from django.http import HttpResponseRedirect


def get_items(request):
    items = Item.objects.all().values()
    return JsonResponse(list(items), safe=False)

# Delete an item
def delete_item(request, item_id):
	item = Item.objects.get(pk=item_id)
	item.is_active = False
	item.save()
	return redirect('shopping_list:list')


def add_item(request):
    if request.method == 'POST':
        add = forms.AddItem(request.POST)
        # save item to db
        if add.is_valid():
            item_name = request.POST['name']
            item, created = Item.objects.get_or_create(name=item_name)
            if created or not item.is_active:
                item.is_active = True
                item.save()
            else:
                # Item already exists and is active
                pass
            
            return redirect('shopping_list:list')
    else:
        add = forms.AddItem()
    
    return render(request, 'shopping_list/list.html', { 'add': add })




def main_shopping_list(request, tag_name=None):
	active_tag = None
	items = Item.objects.all().order_by('updated_at')
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
