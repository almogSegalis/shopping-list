import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from pprint import pprint
import base64
from email.mime.text import MIMEText
import pandas as pd
import re


CLASIFICATION_TIV_TAM = 'tivtaam'
LOGO_TIV = 'https://d226b0iufwcjmj.cloudfront.net/retailers/1062/logo.png?0.11566895948753841'
CLASIFICATION_JONGEL = 'חנויות מחמד'
SHOPPING_TABLE_INDEX = 2
RLEVANT_EMAIL_INDEX = 2

# Set the scope for the Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Load the user's credentials from a file
creds_file = r'/Users/almog/Documents/PycharmProjects/django_project/untitled folder/credentials.json'
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


for message in messages:
    msg = service.users().messages().get(
            userId='me', id=message['id']).execute()
    headers = msg['payload']['headers']
    body = get_message_body(service, msg)
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
    folder_path = "shopping/shopping_list/utils/emails"
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'w') as file:
        file.write(f"Message ID: {message['id']}\n")
        file.write(f"Body:\n{body}\n\n")

# c_tiv=1
# for message in messages:
#     msg = service.users().messages().get(
#             userId='me', id=message['id']).execute()
#     body = get_message_body(service, msg)
#     if CLASIFICATION_TIV_TAM in body:
#         file_name = f'tiv_tam_{c_tiv}.html'
#         c_tiv += 1
#     elif CLASIFICATION_TIV_TAM in body:
#         file_name = f'JONGEL.html'
#     else:
#         file_name = f'None.html'
#     with open("utils/emails/" + file_name, 'w') as file:
#         file.write(f"Message ID: {message['id']}\n")
#         file.write(f"Body:\n{body}\n\n")


# def get_values_table_tiv(file):
#     # Get the valus from the email table
#     dfs = pd.read_html(file, encoding="utf-8")
#     df = dfs[SHOPPING_TABLE_INDEX]
#     df = df[df['Unnamed: 5'].isna()] # remove irrelevent rows.
#     df = df[df.columns[1:5]] # remove irrelevent columns.
#     df.index = pd.Index(range(len(df))) # rebuild index 
#     return df

# def get_items_name_tiv(file):
#     item_list=[]
#     df = get_values_table_tiv(file)
#     for index, value in df['שם'].iteritems():
#         item_list.append(value)
#     with open(f'shopping/shopping_list/utils/list_of_items_tiv_{c_tiv}.txt', 'w') as file:
#         file.write(str(item_list))
#     return item_list

# folder_path = "utils/emails"

# for filename in os.listdir(folder_path):
#     if os.path.isfile(os.path.join(folder_path, filename)):
#         with open(os.path.join(folder_path, filename), "r") as file:
#             content=file.read()
#             if CLASIFICATION_TIV_TAM in content:
#                 get_items_name_tiv("tiv_tam.html")

