from django.shortcuts import render, redirect
from .models import Item, Tag
from . import forms
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt


def update_item(request, item_id):
    item = Item.objects.get(pk=item_id)
    tags = item.tags.all()
    data = [
        {
            'id': item.id,
            'name': item.name,
            'quantity': item.quantity,
            'tags': [
                {'id': tag.id, 'name': tag.name, 'color': tag.color}
                for tag in tags
            ]
        }
    ]
    context = {'data': data}
    return render(request, 'shopping_list/update_item.html', context)    

# Get all items
def get_items(request):
    items = Item.objects.all().items = Item.objects.all().values('id', 'name', 'quantity', 'created_at', 'updated_at', 'is_active', 'tags__id', 'tags__name', 'tags__color')
    return JsonResponse(list(items), safe=False) #return all items

# Delete an item
def delete_item(request, item_id):
	item = Item.objects.get(pk=item_id)
	item.is_active = False
	item.save()
	return JsonResponse(True, safe=False) #return true if delete succeeded

# Update an item's quantity
def update_quantity(request, item_id, quantity):
    item = Item.objects.get(pk=item_id)
    item.quantity = quantity
    item.save()
    return JsonResponse(True, safe=False) #return true if update succeeded

# Add an item
def add_item(request, item_name=None):
    if request.method == 'POST':
        item, created = Item.objects.get_or_create(name=item_name)
        if created or not item.is_active:
            item.is_active = True
            item.save()
        else:
            # Item already exists and is active
            pass
        return JsonResponse(True, safe=False) #return true if add succeeded

# Filter items by tag
def filter_items(request, tag_name):
    items = Item.objects.filter(tags__name=tag_name)
    data = [{'name': item.name, 'quantity': item.quantity} for item in items]
    return JsonResponse({'items': data}) 

# Main shopping list view
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
