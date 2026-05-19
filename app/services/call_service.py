import os

from dotenv import load_dotenv

from twilio.rest import Client


load_dotenv()


ACCOUNT_SID = os.getenv(
    "TWILIO_ACCOUNT_SID"
)

AUTH_TOKEN = os.getenv(
    "TWILIO_AUTH_TOKEN"
)

TWILIO_PHONE = os.getenv(
    "TWILIO_PHONE_NUMBER"
)


client = Client(
    ACCOUNT_SID,
    AUTH_TOKEN
)


def make_reminder_call(
    task_name,
    deadline
):

    user_phone = os.getenv(
        "USER_PHONE_NUMBER"
    )

    twiml_message = f"""
    <Response>
        <Say voice="alice">
            Hello Rudra.

            Reminder for your task.

            {task_name}

            Deadline is {deadline}.

            Please complete it on time.
        </Say>
    </Response>
    """

    call = client.calls.create(

        twiml=twiml_message,

        to=user_phone,

        from_=TWILIO_PHONE
    )

    print("CALL CREATED")
    print(call.sid)

def send_whatsapp_message(
    task_name,
    deadline
):

    user_whatsapp = os.getenv(
        "USER_WHATSAPP_NUMBER"
    )

    twilio_whatsapp = os.getenv(
        "TWILIO_WHATSAPP_NUMBER"
    )

    message = f"""
Hello Rudra 👋

Your AI Executive Assistant reminder.

📌 Task:
{task_name}

📅 Deadline:
{deadline}

📞 You will receive an automated AI reminder call shortly.

Please pick up the call and press any key to accept the voice reminder.
"""

    client.messages.create(

        from_=twilio_whatsapp,

        to=user_whatsapp,

        body=message
    )

    print("WHATSAPP MESSAGE SENT")