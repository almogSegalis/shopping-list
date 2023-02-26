import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from pprint import pprint
import base64
from email.mime.text import MIMEText
import pandas as pd

SHOPPING_TABLE_INDEX = 2
RLEVANT_EMAIL_INDEX = 3

# Set the scope for the Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Load the user's credentials from a file
creds_file = 'credentials.json'
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


with open('messages.html', 'w') as file:

    # Retrieve the content of a specific email message and write it to the file
    def get_message_body(service, message):
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

    for message in [messages[RLEVANT_EMAIL_INDEX]]:
        msg = service.users().messages().get(
            userId='me', id=message['id']).execute()
        body = get_message_body(service, msg)
        file.write(f"Message ID: {message['id']}\n")
        file.write(f"Body:\n{body}\n\n")

def get_values_table_tiv():
    # Get the valus from the email table
    dfs = pd.read_html("messages.html", encoding="utf-8")
    df = dfs[SHOPPING_TABLE_INDEX]
    df = df[df['Unnamed: 5'].isna()] # remove irrelevent rows.
    df = df[df.columns[1:5]] # remove irrelevent columns.
    df.index = pd.Index(range(len(df))) # rebuild index 
    return df

def get_items_name_tiv():
    item_list=[]
    df = get_values_table_tiv()
    for index, value in df['שם'].iteritems():
        item_list.append(value)
    with open('list_of_items.text', 'w') as file:
        file.write(str(item_list))
    return item_list

get_items_name_tiv()