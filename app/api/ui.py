import gradio as gr
from app.env.environment import EmailEnv
from app.models.action import Action
from app.env.environment import extract_tasks_from_email
from app.shared_data import latest_data

env = EmailEnv()



def process_email(email_text):
    try:
        obs = env.reset()

        env.current_email.email = email_text
        env.tasks = extract_tasks_from_email(email_text)
        env.priority = env.detect_priority(email_text)

        tasks = env.tasks

        if tasks:
            response_text = "Thanks for the email. Here’s what I’ll handle:\n\n"
            for t in tasks:
                response_text += f"• {t}\n"

            response_text += "\nI’ll keep you updated once completed."
        else:
            response_text = "No clear task found, I will review it."

        action = Action(
            action_type="reply",
            content=response_text
        )

        obs, reward, done, _ = env.step(action)
        return (
            f"📩 {email_text}",
            f"🤖 {action.content}",
            f"🎯 Score: {reward.score}\nReason: {reward.reason}",
            "\n".join([f"• {t}" for t in tasks]),
            env.priority
        )



    except Exception as e:
        return (
            "ERROR",
            str(e),
            "ERROR",
            "ERROR"
        )

def get_latest_email():
    return (
        latest_data["email"],
        latest_data["action"],
        latest_data["reward"],
        latest_data["tasks"],
        latest_data["priority"]
    )

with gr.Blocks() as demo:
    gr.Markdown("# 📧 AI Email Triage Agent")

    email_input = gr.Textbox(label="Enter Email", lines=10)

    btn = gr.Button("Process")

    output_email = gr.Textbox(label="Email")
    output_action = gr.Textbox(label="Action Taken")
    output_reward = gr.Textbox(label="Reward Score")
    output_tasks = gr.Textbox(label="Extracted Tasks")
    output_priority = gr.Textbox(label="Priority")

    btn.click(
        fn=process_email,
        inputs=email_input,
        outputs=[output_email, output_action, output_reward, output_tasks,output_priority]
    )
    demo.load(
        fn=get_latest_email,
        inputs=None,
        outputs=[output_email, output_action, output_reward, output_tasks,output_priority],

    )

demo.launch()
