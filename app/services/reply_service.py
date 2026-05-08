import random


def generate_ai_reply(
    sender,
    subject,
    email_body,
    tasks,
    priority
):

    greetings = [
        "Thank you for your email.",
        "Thank you for the update.",
        "I appreciate the information.",
        "Thank you for informing me."
    ]

    high_priority_responses = [
        (
            "I have noted the urgent tasks "
            "and will prioritize them immediately."
        ),
        (
            "The tasks have been acknowledged "
            "and will be completed on priority."
        ),
        (
            "I understand the urgency and "
            "will ensure timely completion."
        )
    ]

    medium_priority_responses = [
        (
            "The tasks have been noted and "
            "will be completed accordingly."
        ),
        (
            "I have acknowledged the requirements "
            "and will work on them soon."
        )
    ]

    low_priority_responses = [
        (
            "The information has been noted."
        ),
        (
            "Thank you. I have acknowledged the update."
        )
    ]

    no_task_responses = [
        (
            "The email has been acknowledged."
        ),
        (
            "Thank you for the information."
        )
    ]

    greeting = random.choice(greetings)

    if "No task required" in tasks:

        body = random.choice(
            no_task_responses
        )

    elif priority.lower() == "high":

        body = random.choice(
            high_priority_responses
        )

    elif priority.lower() == "medium":

        body = random.choice(
            medium_priority_responses
        )

    else:

        body = random.choice(
            low_priority_responses
        )

    task_summary = ""

    if (
        tasks
        and "No task required" not in tasks
    ):

        task_summary = (
            "\n\nTasks noted:\n- "
            + "\n- ".join(tasks)
        )

    reply = f"""
Dear Sender,

{greeting}

{body}

{task_summary}

Regards,
Rudra
"""

    return reply.strip()