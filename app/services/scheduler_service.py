from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from app.services.call_service import make_reminder_call, send_whatsapp_message

scheduler = BackgroundScheduler()
scheduler.start()

def schedule_deadline_calls(task_name, deadline_datetime):
    """
    1. Immediate reminder (as soon as email is processed)
    2. Pre-deadline reminders: 2 days before, twice a day
    """

    now = datetime.now()

    # ----------------------
    # 1. Immediate reminder
    # ----------------------
    scheduler.add_job(
        lambda: [
            send_whatsapp_message(
                task_name,
                deadline_datetime.strftime("%d-%m-%Y")
            ),
            make_reminder_call(
                task_name,
                deadline_datetime.strftime("%d-%m-%Y")
            )
        ],
        'date',
        run_date=now + timedelta(seconds=5)  # 5 seconds after processing for demo
    )

    # --------------------------
    # 2. Pre-deadline reminders
    # --------------------------
    reminder_day = deadline_datetime - timedelta(days=2)

    # Morning call at 10 AM
    morning_call = reminder_day.replace(hour=10, minute=0, second=0)

    # Evening call at 6 PM
    evening_call = reminder_day.replace(hour=18, minute=0, second=0)

    # Schedule morning pre-deadline reminder
    scheduler.add_job(
        lambda: [
            send_whatsapp_message(
                task_name,
                deadline_datetime.strftime("%d-%m-%Y")
            ),
            make_reminder_call(
                task_name,
                deadline_datetime.strftime("%d-%m-%Y")
            )
        ],
        'date',
        run_date=morning_call
    )

    # Schedule evening pre-deadline reminder
    scheduler.add_job(
        lambda: [
            send_whatsapp_message(
                task_name,
                deadline_datetime.strftime("%d-%m-%Y")
            ),
            make_reminder_call(
                task_name,
                deadline_datetime.strftime("%d-%m-%Y")
            )
        ],
        'date',
        run_date=evening_call
    )

    print(f"Immediate + Pre-deadline reminders scheduled for task: {task_name}")