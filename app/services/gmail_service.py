import os
import base64
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


def gmail_authenticate():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file(
            'token.json',
            SCOPES
        )

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json',
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build(
        'gmail',
        'v1',
        credentials=creds
    )

    return service


def get_unread_emails(service):
    results = service.users().messages().list(
        userId='me',
        labelIds=['INBOX'],
        q='is:unread'
    ).execute()

    messages = results.get('messages', [])

    return messages


def read_email(service, msg_id):
    message = service.users().messages().get(
        userId='me',
        id=msg_id,
        format='full'
    ).execute()

    payload = message['payload']

    headers = payload.get('headers', [])

    subject = ''

    for header in headers:
        if header['name'] == 'Subject':
            subject = header['value']

    body = ''

    if 'parts' in payload:
        parts = payload['parts']

        for part in parts:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data')

                if data:
                    body = base64.urlsafe_b64decode(
                        data
                    ).decode('utf-8')

    else:
        data = payload['body'].get('data')

        if data:
            body = base64.urlsafe_b64decode(
                data
            ).decode('utf-8')

    return {
        'subject': subject,
        'body': body
    }


def mark_as_read(service, msg_id):
    service.users().messages().modify(
        userId='me',
        id=msg_id,
        body={
            'removeLabelIds': ['UNREAD']
        }
    ).execute()


def send_reply(service, to, subject, message_text):
    message = MIMEText(message_text)

    message['to'] = to
    message['subject'] = f'Re: {subject}'

    raw = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    body = {'raw': raw}

    service.users().messages().send(
        userId='me',
        body=body
    ).execute()