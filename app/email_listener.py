import time
from app.services.todo_service import (
    add_tasks,
    show_tasks
)

from app.services.gmail_service import (
    gmail_authenticate,
    get_unread_emails,
    read_email,
    mark_as_read
)

from app.env.environment import (
    EmailEnv,
    process_real_email
)


service = gmail_authenticate()

env = EmailEnv()


def process_email(email_data):

    subject = email_data['subject']

    body = email_data['body']

    print('\n==============================')
    print(f'Subject: {subject}')
    print('==============================')

    result = process_real_email(
        env,
        body
    )

    add_tasks(
        result['tasks'],
        result['priority']
    )

    print('\nExtracted Tasks:')

    if result['tasks']:

        for task in result['tasks']:
            print('-', task)

    else:
        print('No tasks found.')

    print(f"\nPriority: {result['priority']}")

    show_tasks()

    print('==============================\n')


while True:

    print('\nChecking Gmail Inbox...')

    unread_messages = get_unread_emails(service)

    if not unread_messages:
        print('No unread emails.')

    for msg in unread_messages:

        email_data = read_email(
            service,
            msg['id']
        )

        process_email(email_data)

        mark_as_read(
            service,
            msg['id']
        )

    time.sleep(20)