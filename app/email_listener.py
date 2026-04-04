import time
import imaplib
import email
from email.header import decode_header
from app.shared_data import latest_data

from app.env.environment import EmailEnv, extract_tasks_from_email
from app.models.action import Action

EMAIL = "kishansingh2801@gmail.com"
PASSWORD = "ybdfbddzudzqpniy"

env = EmailEnv()


def read_emails():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")

    # Get unread emails
    status, messages = mail.search(None, "UNSEEN")

    email_ids = messages[0].split()

    for eid in email_ids:
        _, msg_data = mail.fetch(eid, "(RFC822)")
        raw_email = msg_data[0][1]

        msg = email.message_from_bytes(raw_email)

        # Decode subject
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")

        print("\n📧 NEW EMAIL:", subject)

        # Get body
        body = ""

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
        else:
            body = msg.get_payload(decode=True).decode()

        process_email(body)


def process_email(email_text):
    env.reset()

    env.current_email.email = email_text
    env.tasks = extract_tasks_from_email(email_text)
    env.priority = env.detect_priority(email_text)

    tasks = env.tasks

    if tasks:
        response_text = "🤖 I will handle:\n"
        for t in tasks:
            response_text += f"- {t}\n"
    else:
        response_text = "No clear task found."

    action = Action(
        action_type="reply",
        content=response_text
    )

    _, reward, _, _ = env.step(action)
    

    latest_data["email"] = email_text
    latest_data["action"] = response_text
    latest_data["reward"] = f"{reward.score} ({reward.reason})"
    latest_data["tasks"] = str(tasks)
    latest_data["priority"] = env.priority
    
    print("updated:",latest_data)

    print("📄 Email Content:\n", email_text)
    print("🧠 Tasks:", tasks)
    print("⚡ Priority:", env.priority)
    print("🤖 Action:\n", response_text)
    print("🎯 Reward:", reward.score)
    print("-" * 50)


if __name__ == "__main__":
    while True:
        print("🔄 Checking for new emails...")
        read_emails()
        time.sleep(20)