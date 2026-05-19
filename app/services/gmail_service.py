import os
import base64
from bs4 import BeautifulSoup

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    "https://www.googleapis.com/auth/calendar"
]


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





import base64
from bs4 import BeautifulSoup


def read_email(service, message_id):

    message = service.users().messages().get(
        userId='me',
        id=message_id,
        format='full'
    ).execute()

    payload = message.get('payload', {})

    headers = payload.get('headers', [])

    subject = "No Subject"
    sender = "Unknown Sender"

    for header in headers:

        if header['name'] == 'Subject':
            subject = header['value']

        elif header['name'] == 'From':
            sender = header['value']

    body = ""

    # Recursive extractor
    def extract_body(part):

        mime_type = part.get("mimeType", "")

        body_data = part.get("body", {}).get("data")

        # TEXT PLAIN
        if mime_type == "text/plain" and body_data:

            try:
                decoded = base64.urlsafe_b64decode(
                    body_data
                ).decode(
                    "utf-8",
                    errors="ignore"
                )

                return decoded

            except Exception:
                return ""

        # HTML EMAIL
        if mime_type == "text/html" and body_data:

            try:
                decoded = base64.urlsafe_b64decode(
                    body_data
                ).decode(
                    "utf-8",
                    errors="ignore"
                )

                soup = BeautifulSoup(
                    decoded,
                    "html.parser"
                )

                return soup.get_text(
                    separator="\n"
                )

            except Exception:
                return ""

        # MULTIPART EMAILS
        parts = part.get("parts", [])

        for p in parts:

            result = extract_body(p)

            if result:
                return result

        return ""

    body = extract_body(payload)

    # Fallback if still empty
    if not body.strip():

        snippet = message.get("snippet", "")

        body = snippet

    return {
        "subject": subject,
        "sender": sender,
        "body": body.strip()
    }


def mark_as_read(service, msg_id):

    service.users().messages().modify(
        userId='me',
        id=msg_id,
        body={
            'removeLabelIds': ['UNREAD']
        }
    ).execute()