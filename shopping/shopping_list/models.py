from django.utils import timezone
from django.db import models
import ast
import os
import datetime
import pandas as pd
import re

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
    venue_name = models.ForeignKey(Tag, blank=True, null=True, on_delete=models.CASCADE)
    order_time = models.DateTimeField()
    order_num =  models.IntegerField(max_length=100, default='')

    # Field for items in the order
    items = models.ManyToManyField(Item)

    def __str__(self):
        return f'Order {self.id} - {self.venue_name} - {self.order_time}  - {self.order_num}'

# --- add previous orders from emails ---
SHOPPING_TABLE_INDEX = 2
folder_path = "shopping_list/utils/emails"

def get_values_table_tiv(file):
    # Get the valus from the email table
    dfs = pd.read_html(file, encoding="utf-8")
    df = dfs[SHOPPING_TABLE_INDEX]
    df = df[df['Unnamed: 5'].isna()] # remove irrelevent rows.
    df = df[df.columns[1:5]] # remove irrelevent columns.
    df.index = pd.Index(range(len(df))) # rebuild index 
    return df

def get_items_name_tiv(file):
    item_list=[]
    df = get_values_table_tiv(file)
    for index, value in df['שם'].iteritems():
        item_list.append(value)
    return item_list


# inisialize the orders with data from emails
for filename in os.listdir(folder_path):
    if os.path.isfile(os.path.join(folder_path, filename)):
        if filename != '.DS_Store':
            file_path = os.path.join(folder_path, filename)
            if 'tiv_tam' in filename:
                items = get_items_name_tiv(file_path)
                s = filename
                # Extract the date and time values using regular expressions
                msg_id = re.search(r"_id_([0-9]+)", s).group(1)
                date_str = re.search(r'_date_([0-9]{2}-[0-9]{2}-[0-9]{4})_', s).group(1)
                time_str = re.search(r'_time_([0-9]{2}-[0-9]{2})', s).group(1)
                
                # Convert the date and time strings to datetime objects
                order_datetime = datetime.datetime.strptime(f'{date_str} {time_str}', '%d-%m-%Y %H-%M')

                # Convert the datetime object to local timezone
                order_time = timezone.localtime(timezone.make_aware(order_datetime))

                # Check if the order already exists
                existing_order = Order.objects.filter(order_time=order_time).first()

                # Get the specific tag to add to the item
                tag_name = "טיב טעם"
                tag = Tag.objects.filter(name=tag_name).first()

                if existing_order:
                    # Order already exists, skip creating a new one and add items to existing order
                    order = existing_order
                else:
                    # Order does not exist, create a new one
                    order = Order.objects.create(venue_name=tag, order_time=order_time, order_num=msg_id)

                for item_name in items:
                    item, created = Item.objects.get_or_create(name=item_name)
                    if created:
                        item.is_active = False
                        item.tags.add(tag)
                        item.save()
                        order.items.add(item)
                    else:
                        # Handle the case where the item exist
                        item.tags.add(tag)
                        item.save()
                        order.items.add(item)