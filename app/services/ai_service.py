import re


def extract_tasks_from_email(email_text):
    patterns = [
        r'please (.+)',
        r'kindly (.+)',
        r'complete (.+)',
        r'submit (.+)',
        r'attend (.+)',
        r'prepare (.+)',
        r'send (.+)'
    ]

    tasks = []

    for pattern in patterns:
        matches = re.findall(
            pattern,
            email_text.lower()
        )

        for match in matches:
            cleaned = match.strip()

            if cleaned not in tasks:
                tasks.append(cleaned)

    return tasks


def detect_priority(email_text):
    urgent_keywords = [
        'urgent',
        'asap',
        'important',
        'critical',
        'deadline',
        'immediately'
    ]

    email_text = email_text.lower()

    for word in urgent_keywords:
        if word in email_text:
            return 'HIGH'

    return 'NORMAL'