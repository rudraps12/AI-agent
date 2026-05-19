from googleapiclient.discovery import build

from google.oauth2.credentials import Credentials

from datetime import datetime, timedelta


SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/calendar"
]


def get_calendar_service():

    creds = Credentials.from_authorized_user_file(
        "token.json",
        SCOPES
    )

    service = build(
        "calendar",
        "v3",
        credentials=creds
    )

    return service


def create_calendar_event(
    title,
    deadline_date,
    description=""
):
    print("CALENDAR FUNCTION CALLED")
    
    service = get_calendar_service()

    start_time = datetime.strptime(
        deadline_date,
        "%d-%m-%Y"
    )

    end_time = start_time + timedelta(hours=1)

    event = {

        "summary": title,
        "description" : description,

        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": "Asia/Kolkata",
        },

        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": "Asia/Kolkata",
        },
    }

    event_result = service.events().insert(
        calendarId='primary',
        body=event
    ).execute()

    return event_result.get(
        'htmlLink'
    )