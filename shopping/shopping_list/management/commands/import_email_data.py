from django.core.management.base import BaseCommand, CommandError
from shopping_list.models import Item, Tag, Order
from django.utils import timezone

import pandas as pd

import os
import datetime
import re

import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from pprint import pprint
import base64
from email.mime.text import MIMEText

CLASIFICATION_TIV_TAM = 'tivtaam'
LOGO_TIV = 'https://d226b0iufwcjmj.cloudfront.net/retailers/1062/logo.png?0.11566895948753841'
CLASIFICATION_JONGEL = 'חנויות מחמד'
SHOPPING_TABLE_INDEX = 2
RLEVANT_EMAIL_INDEX = 2

# Set the scope for the Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


# --- add previous orders from emails ---
SHOPPING_TABLE_INDEX = 2

# Retrieve the content of a specific email message and write it to the file
def get_message_body(message):
    payload = message['payload']
    parts = payload.get('parts', [])
    data = None
    for part in parts:
        if part['mimeType'] == 'text/html':
            data = part['body']['data']
            break
    if data is None:
        data = payload['body'].get('data', '')
    body = base64.urlsafe_b64decode(data).decode('utf-8')
    return body

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
        # Load the user's credentials from a file
        creds_file = r'credentials.json'
        creds = None
        if os.path.exists('token.json'):
            with open('token.json', 'r') as token_file:
                creds_data = token_file.read()
                creds = Credentials.from_authorized_user_info(
                    info=json.loads(creds_data), scopes=SCOPES)

        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
            creds = flow.run_local_server(port=4000)

            # Save the credentials to a file
            with open('token.json', 'w') as token_file:
                token_file.write(creds.to_json())

        # Create a Gmail API client
        service = build('gmail', 'v1', credentials=creds)

        results = service.users().messages().list(userId='me').execute()
        messages = results.get('messages', [])

        for message in messages:
            msg = service.users().messages().get(
                    userId='me', id=message['id']).execute()
            headers = msg['payload']['headers']
            body = get_message_body(msg)
            email_subject = next((header['value'] for header in headers if header['name'] == 'Subject'), None)
            if (CLASIFICATION_TIV_TAM in body) or (LOGO_TIV in body):
                update = False
                if "עדכון" in email_subject:
                    update = True
                pattern = r"\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}"
                date_str = re.search(pattern, email_subject).group(0)
                pattern = r"#\d+"
                order_id = re.search(pattern, email_subject).group(0)
                prefix = "#"
                order_id = order_id.removeprefix(prefix)
                date_str = date_str.replace('/','-').replace(' ', '_time_').replace(':', '-')
                if update:    
                    file_name = f'tiv_tam_update_date_{date_str}_id_{order_id}.html'
                else:
                    file_name = f'tiv_tam_date_{date_str}_id_{order_id}.html'
            elif CLASIFICATION_JONGEL in email_subject:
                file_name = f'JONGEL.html'
            else:
                file_name = f'None.html'
            folder_path = "shopping_list/utils/emails/"
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'w') as file:
                file.write(f"Message ID: {message['id']}\n")
                file.write(f"Body:\n{body}\n\n")


        ###################################################################################################
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