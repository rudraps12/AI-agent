import pandas as pd
import gradio as gr

from app.services.reply_service import (
    generate_ai_reply
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

from app.services.todo_service import (
    add_tasks,
    get_tasks,
    clear_tasks
)


service = gmail_authenticate()

env = EmailEnv()
email_cache = []



current_email_index = 0


def process_latest_emails():

    global email_cache
    global current_email_index

    unread_messages = get_unread_emails(service)

    unread_messages = unread_messages[:5]

    email_cache = []

    for msg in unread_messages:

        email_data = read_email(
            service,
            msg['id']
        )

        email_cache.append(email_data)

    current_email_index = 0

    return display_email(
        current_email_index
    )


def process_manual_email(email_text):

    clear_tasks()

    result = process_real_email(
        env,
        email_text
    )

    add_tasks(
        result['tasks'],
        result['priority']
    )

    reply_text = generate_ai_reply(
        sender="User Input",
        subject="Manual Email",
        email_body=email_text,
        tasks=result['tasks'],
        priority=result['priority']
    )

    dataframe = pd.DataFrame(
        get_tasks()
    )

    return (
        "Manual Email",
        "User Input",
        result['priority'],
        dataframe,
        reply_text
    )

def display_email(index):

    global email_cache

    if not email_cache:

        empty_df = pd.DataFrame(
            columns=["task", "priority", "status"]
        )

        return (
            "No unread emails found.",
            "No Sender",
            "NONE",
            empty_df,
            "No AI reply generated."
        )

    if index < 0:

        empty_df = pd.DataFrame(
            columns=["task", "priority", "status"]
        )

        return (
            "No previous unread email.",
            "",
            "",
            empty_df,
            ""
        )

    if index >= len(email_cache):

        empty_df = pd.DataFrame(
            columns=["task", "priority", "status"]
        )

        return (
            "No next unread email.",
            "",
            "",
            empty_df,
            ""
        )

    clear_tasks()

    email_data = email_cache[index]

    subject = email_data['subject']

    sender = email_data['sender']

    body = email_data['body']

    result = process_real_email(
        env,
        body
    )

    add_tasks(
        result['tasks'],
        result['priority']
    )

    reply_text = generate_ai_reply(
        sender=sender,
        subject=subject,
        email_body=body,
        tasks=result['tasks'],
        priority=result['priority']
    )

    dataframe = pd.DataFrame(
        get_tasks()
    )

    return (
        subject,
        sender,
        result['priority'],
        dataframe,
        reply_text
    )

def next_email():

    global current_email_index

    current_email_index += 1

    return display_email(
        current_email_index
    )


def previous_email():

    global current_email_index

    current_email_index -= 1

    return display_email(
        current_email_index
    )


with gr.Blocks(theme=gr.themes.Soft()) as demo:

    gr.Markdown(
        "# Gmail AI Executive Assistant"
    )

    gr.Markdown(
        "AI powered email automation dashboard"
    )

    with gr.Row():

        subject_output = gr.Textbox(
            label="Latest Email Subject"
        )

        sender_output = gr.Textbox(
            label="Sender"
        )

        priority_output = gr.Textbox(
            label="Detected Priority"
        )

    tasks_output = gr.Dataframe(
        headers=[
            "task",
            "priority",
            "status"
        ],
        label="Generated Todo List"
    )

    reply_output = gr.Textbox(
        label="AI Generated Reply",
        lines=8
    )

    gr.Markdown("## Manual Email Testing")

    manual_input = gr.Textbox(
        lines=10,
        placeholder="Paste email content here..."
    )

    manual_button = gr.Button(
        "Process Manual Email"
    )

    gmail_button = gr.Button(
        "Load Latest 5 Unread Emails"
    )

    next_button = gr.Button(
        "Next Email"
    )

    previous_button = gr.Button(
        "Previous Email"
    )

    manual_button.click(
        fn=process_manual_email,
        inputs=[manual_input],
        outputs=[
            subject_output,
            sender_output,
            priority_output,
            tasks_output,
            reply_output
        ]
    )

    gmail_button.click(
        fn=process_latest_emails,
        inputs=[],
        outputs=[
            subject_output,
            sender_output,
            priority_output,
            tasks_output,
            reply_output
        ]
    )

    next_button.click(
        fn=next_email,
        inputs=[],
        outputs=[
            subject_output,
            sender_output,
            priority_output,
            tasks_output,
            reply_output
        ]
    )

    previous_button.click(
        fn=previous_email,
        inputs=[],
        outputs=[
            subject_output,
            sender_output,
            priority_output,
            tasks_output,
            reply_output
        ]
    )


demo.launch()