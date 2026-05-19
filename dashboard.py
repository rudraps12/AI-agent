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
        email_text,
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
            "No email content",
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
    latest_priority = result['priority']

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
        latest_priority,
        body,
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


custom_css = """
body {
    background: linear-gradient(
        135deg,
        #0f172a,
        #111827,
        #1e293b
    );
    font-family: 'Poppins', sans-serif;
}

/* Main container */
.gradio-container {
    background: transparent !important;
}

/* Cards */
.block {
    border-radius: 20px !important;
    background: rgba(255,255,255,0.08) !important;
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    transition: all 0.3s ease;
}

.block:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(0,255,255,0.25);
}

/* Buttons */
button {
    background: linear-gradient(
        135deg,
        #06b6d4,
        #3b82f6
    ) !important;

    color: white !important;

    border: none !important;

    border-radius: 14px !important;

    font-weight: bold !important;

    transition: all 0.3s ease !important;

    box-shadow: 0 0 20px rgba(59,130,246,0.5);
}

/* Button hover effect */
button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 30px rgba(0,255,255,0.9);
}

/* Textboxes */
textarea,
input {
    background: rgba(255,255,255,0.08) !important;
    color: white !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
}

/* Labels */
label {
    color: #e2e8f0 !important;
    font-weight: 600;
}

/* Headers */
h1, h2, h3 {
    color: white !important;
    text-align: center;
}

/* Dataframe */
table {
    border-radius: 12px !important;
    overflow: hidden;
}

/* Smooth animations */
* {
    transition: all 0.25s ease;
}
/* Compact centered buttons */

/* Main Action Buttons Only */

button.primary-btn {

    height: 44px !important;

    width: 40% !important;

    margin: 10px auto !important;

    border-radius: 14px !important;

    font-size: 15px !important;

    font-weight: 600 !important;

    background: linear-gradient(
        135deg,
        #06b6d4,
        #3b82f6
    ) !important;

    color: white !important;

    border: none !important;

    transition: all 0.3s ease !important;

    box-shadow: 0 0 15px rgba(59,130,246,0.45);

    display: block !important;
}

button.primary-btn:hover {

    transform: scale(1.03);

    box-shadow: 0 0 28px rgba(0,255,255,0.7);
}

/* Fix dataframe toolbar */

table button,
thead button,
tbody button {

    width: auto !important;

    height: auto !important;

    min-height: auto !important;

    margin: 0 !important;

    box-shadow: none !important;

    background: transparent !important;
}

/* Section cards */

.gr-box,
.block {

    padding: 16px !important;
}
/* Small elegant labels */

label {

    font-size: 13px !important;

    letter-spacing: 0.5px;

    color: #94a3b8 !important;
}
"""

with gr.Blocks(
    theme=gr.themes.Soft(),
    css=custom_css
) as demo:

    gr.Markdown(
        """
        <div style='text-align:center;padding:20px;'>

        <h1 style='font-size:55px;
                background: linear-gradient(
                    90deg,
                    #06b6d4,
                    #3b82f6,
                    #8b5cf6
                );
                -webkit-background-clip:text;
                -webkit-text-fill-color:transparent;
                font-weight:900;'>

        Gmail AI Executive Assistant

        </h1>

        <p style='color:#cbd5e1;
                font-size:18px;'>

        AI-Powered Productivity & Email Automation Platform

        </p>

        </div>
        """
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
    
    original_email_output = gr.Textbox(
        label="Original Email Content",
        lines=10 
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
        lines=8,
        placeholder="Paste email content here...",
        label="Manual Email Testing"
    )

    manual_button = gr.Button(
        "⚡ Process Manual Email",
        elem_classes="primary-btn"
    )

    gmail_button = gr.Button(
        "📥 Load Latest 5 Emails",
        elem_classes="primary-btn"
    )
    
    next_button = gr.Button(
        "➡ Next Email",
        elem_classes="primary-btn"
    )

    previous_button = gr.Button(
        "⬅ Previous Email",
        elem_classes="primary-btn"
    )

    manual_button.click(
        fn=process_manual_email,
        inputs=[manual_input],
        outputs=[
            subject_output,
            sender_output,
            priority_output,
            original_email_output,
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
            original_email_output,
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
            original_email_output,
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
            original_email_output,
            tasks_output,
            reply_output
        ]
    )


demo.launch(
    favicon_path=None
)