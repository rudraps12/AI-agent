import gradio as gr
from app.env.environment import EmailEnv, extract_tasks_from_email

env = EmailEnv()


def process_email(email_text):
    try:
        env.reset()

        env.current_email.email = email_text
        tasks = extract_tasks_from_email(email_text)
        priority = env.detect_priority(email_text)

        if tasks:
            task_list = "\n".join([f"• {t}" for t in tasks])

            response = f"""
📧 Email Analysis

🧠 Detected Tasks:
{task_list}

⚡ Priority: {priority}

🤖 Suggested Reply:
Thanks for your email. I will handle the following:
{task_list}

I'll keep you updated once completed.
"""
        else:
            response = f"""
📧 Email Analysis

❌ No clear tasks detected

⚡ Priority: {priority}

🤖 Suggested Reply:
Thanks for your message. Could you please provide more details?
"""

        return response

    except Exception as e:
        return f"❌ Error: {str(e)}"


# 🔥 PREMIUM UI
with gr.Blocks(theme=gr.themes.Glass()) as demo:

    gr.Markdown("# ✉️ AI Email Triage System")
    gr.Markdown("Smart email analysis with task detection & priority scoring")

    with gr.Row():
        with gr.Column(scale=2):
            email_input = gr.Textbox(
                label="📩 Enter Email",
                placeholder="Paste your email here...",
                lines=10
            )

            analyze_btn = gr.Button("🚀 Analyze Email", variant="primary")

        with gr.Column(scale=2):
            output = gr.Textbox(
                label="📊 Analysis Result",
                lines=15
            )

    analyze_btn.click(process_email, inputs=email_input, outputs=output)

