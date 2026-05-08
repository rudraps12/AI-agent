import gradio as gr

from app.api.logic import build_triage


SAMPLE_EMAIL = """Urgent: please attend the project sync at 5 PM and send the release report ASAP.
Also reschedule the client follow-up if there is a calendar conflict."""


def process_email(email_text, subject, sender):
    email_text = (email_text or "").strip()
    subject = (subject or "Inbox message").strip()
    sender = (sender or "sender@example.com").strip()

    if not email_text:
        return (
            "No email provided",
            "low",
            "archive",
            "No clear action items found.",
            "Paste an email to generate a reply.",
        )

    result = build_triage(email_text, subject=subject, sender=sender)
    tasks = result["tasks"]
    task_text = "\n".join(f"{index + 1}. {task}" for index, task in enumerate(tasks))
    if not task_text:
        task_text = "No clear action items found."

    conflict_note = " Scheduling conflict detected." if result["has_conflict"] else ""
    summary = (
        f"From: {result['sender']}\n"
        f"Subject: {result['subject']}\n"
        f"Priority: {result['priority'].upper()}{conflict_note}"
    )

    return (
        summary,
        result["priority"],
        result["recommended_action"],
        task_text,
        result["suggested_reply"],
    )


with gr.Blocks(title="OpenEnv Email Triage") as demo:
    gr.Markdown("# OpenEnv Email Triage")
    gr.Markdown("Analyze an email, extract tasks, rank priority, and draft a reply.")

    with gr.Row():
        with gr.Column(scale=3):
            sender_input = gr.Textbox(label="Sender", value="boss@company.com")
            subject_input = gr.Textbox(label="Subject", value="Work update")
            email_input = gr.Textbox(
                label="Email",
                value=SAMPLE_EMAIL,
                lines=10,
                placeholder="Paste an email body here",
            )
            analyze_btn = gr.Button("Analyze Email", variant="primary")

        with gr.Column(scale=2):
            summary_output = gr.Textbox(label="Triage Summary", lines=4)
            priority_output = gr.Label(label="Priority")
            action_output = gr.Label(label="Recommended Action")
            tasks_output = gr.Textbox(label="Detected Tasks", lines=7)

    reply_output = gr.Textbox(label="Suggested Reply", lines=9)

    analyze_btn.click(
        process_email,
        inputs=[email_input, subject_input, sender_input],
        outputs=[
            summary_output,
            priority_output,
            action_output,
            tasks_output,
            reply_output,
        ],
    )

    demo.load(
        process_email,
        inputs=[email_input, subject_input, sender_input],
        outputs=[
            summary_output,
            priority_output,
            action_output,
            tasks_output,
            reply_output,
        ],
    )


if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)
