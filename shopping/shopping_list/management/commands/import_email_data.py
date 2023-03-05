from django.core.management.base import BaseCommand, CommandError
from shopping_list.models import Item, Tag, Order
from django.utils import timezone

import pandas as pd

import os
import datetime
import re

# --- add previous orders from emails ---
SHOPPING_TABLE_INDEX = 2
folder_path = "shopping_list/utils/emails"

def get_values_table_tiv(file):
    # Get the valus from the email table
    dfs = pd.read_html(file, encoding="utf-8")
    df = dfs[SHOPPING_TABLE_INDEX]
    # take last column, it must be artficial column created by html table formating
    artficial_column_name = df.columns[-1]
    df = df[df[artficial_column_name].isna()] # remove irrelevent rows.
    df = df[df.columns[1:5]] # remove irrelevent columns.
    df.index = pd.Index(range(len(df))) # rebuild index 
    return df

def get_items_name_tiv(file):
    item_list=[]
    df = get_values_table_tiv(file)
    for index, value in df['שם'].iteritems():
        item_list.append(value)
    return item_list


def deleteUpdateFile(folder_path, update_file, msg_id):
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, update_file)):
            if update_file != '.DS_Store':
                file_path2 = os.path.join(folder_path, filename)
                if msg_id in filename and 'update' not in filename:
                    os.remove(file_path2)

class Command(BaseCommand):
    help = "Imports order data from gmail"

    def handle(self, *args, **options):
        # inisialize the orders with data from emails
        for filename in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, filename)):
                if filename != '.DS_Store':
                    file_path = os.path.join(folder_path, filename)
                    if 'tiv_tam' in filename:
                        update = False
                        items = get_items_name_tiv(file_path)
                        s = filename
                        # Extract the date and time values using regular expressions
                        msg_id = re.search(r"_id_([0-9]+)", s).group(1)
                        date_str = re.search(r'_date_([0-9]{2}-[0-9]{2}-[0-9]{4})_', s).group(1)
                        time_str = re.search(r'_time_([0-9]{2}-[0-9]{2})', s).group(1)
                        if ('update') in s:
                            deleteUpdateFile(folder_path,filename, msg_id)

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