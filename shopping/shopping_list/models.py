from django.db import models
import ast

class Tag(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=50) # bootstrap color
    
    def __str__(self):
        return self.name

class ItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class Item(models.Model):
    name = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    venue_name = models.ForeignKey(Tag, blank=True, null=True, on_delete=models.SET_NULL)
    customer_address = models.CharField(max_length=200)
    order_time = models.DateTimeField(auto_now_add=True)

    # Field for items in the order
    items = models.ManyToManyField(Item)

    def __str__(self):
        return f'Order {self.id} - {self.venue_name} - {self.order_time}'

with open('shopping_list/utils/list_of_items.txt', 'r') as file:
    string_items_list = file.read()
    items_list = ast.literal_eval(string_items_list)
    tag = None
    try:
        tags = Tag.objects.get(name='טיב טעם')
    except Tag.DoesNotExist:
        pass
    except Tag.MultipleObjectsReturned:
        pass
    if tag is not None:
        for item_name in items_list:
            item, created = Item.objects.get_or_create(name=item_name)
            if created:
                item.tags.add(tag)
    else:
        # handel the case the tag doesnot exist
        for item_name in items_list:
            item = Item.objects.get_or_create(name=item_name)

    
