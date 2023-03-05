from django.db import models


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'Item {self.name}'

class Order(models.Model):
    venue_name = models.ForeignKey(Tag, blank=True, null=True, on_delete=models.CASCADE)
    order_time = models.DateTimeField()
    order_num =  models.IntegerField(default='')

    # Field for items in the order
    items = models.ManyToManyField(Item)

    def __str__(self):
        return f'Order {self.id} - {self.venue_name} - {self.order_time}  - {self.order_num}'
