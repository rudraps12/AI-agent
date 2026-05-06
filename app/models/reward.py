import random
from app.models.observation import Observation
from app.models.action import Action
from app.models.reward import Reward
import re
from datetime import datetime

def get_task_type(email_text):
    if "urgent" in email_text.lower():
        return "priority"
    elif "call" in email_text.lower() or "submit" in email_text.lower():
        return "task_extraction"
    else:
        return "action_decision"

def grade_task(task_type, output):
    text = (output or "").lower()

    if task_type == "task_extraction":
        raw = 0.88 if text.strip() else 0.30

    elif task_type == "priority":
        raw = 0.92 if any(x in text for x in ["high", "medium", "low", "urgent", "asap"]) else 0.20

    elif task_type == "action_decision":
        raw = 0.85 if any(x in text for x in ["reply", "escalate", "ignore", "respond", "schedule"]) else 0.20

    else:
        raw = 0.50

    return round(max(0.01, min(0.99, raw)), 4)
def extract_tasks_from_email(email_text):
    tasks = []
    text = email_text.lower()

    sentences = re.split(r'[.!?]', text)

    action_words = [
        "send", "submit", "prepare", "update",
        "complete", "finish", "review", "create",
        "attend", "write", "solve"
    ]
    ignore_words = [
        "you are informed", "kindly ensure", "all questions are",
        "the assignment is"
    ]

    for sentence in sentences:
        sentence = sentence.strip()

        if not sentence:
            continue

        if sentence.startswith(("hi", "hello", "thanks")):
            continue
        if any(phrase in sentence for phrase in ignore_words):
            continue

        for word in action_words:
            if word in sentence:
                cleaned = sentence.replace("please", "").replace("also", "").replace("kindly", "").strip()
                tasks.append(cleaned)
                break

    if "deadline" in text:
        tasks.append("complete before deadline")

    unique_tasks = []
    for t in tasks:
        if t not in unique_tasks:
            unique_tasks.append(t)

    if "asap" in text or "urgent" in text:
    if "handle urgently" not in unique_tasks:
        unique_tasks.append("handle urgently")

return unique_tasks   


class EmailEnv:

    def __init__(self):
        self.current_email = None
        self.done = False
        self.history = []
        self.tasks = []
        self.calendar = []
        self.priority = "low"

    def generate_email(self):
        emails = [
            "Urgent: attend meeting at 5 PM and send report ASAP",
            "Reminder to send report before deadline",
            "Can we reschedule the meeting to 6 PM?",
            "Please schedule a meeting and prepare report",
            "ASAP: finish the report and attend meeting"
        ]
        return random.choice(emails)

    def detect_priority(self, email: str):
        date_match = re.search(r'(\d{1,2}\s+[a-zA-Z]+\s+\d{4})', email)

        if date_match:
            try:
                deadline_str = date_match.group()
                deadline_date = datetime.strptime(deadline_str, "%d %B %Y")
                today = datetime.today()
                diff = (deadline_date - today).days

                if diff <= 2:
                    return "high"
                elif diff <= 5:
                    return "medium"
                else:
                    return "low"
            except:
                pass

        return "low"

    def check_conflict(self, email: str):
        if "5 pm" in email.lower():
            for event in self.calendar:
                if "5 PM" in event:
                    return True
        return False

    def reset(self):
        email_text = self.generate_email()
        self.tasks = extract_tasks_from_email(email_text)
        self.priority = self.detect_priority(email_text)
        self.calendar = ["Meeting at 5 PM"]

        self.current_email = Observation(
            email=email_text,
            sender="boss@company.com",
            subject="Work update",
            history=self.history,
            current_tasks=self.tasks,
            calendar=self.calendar
        )

        self.done = False
        return self.current_email

    def step(self, action: Action):
        task_type = get_task_type(self.current_email.email)
        result = getattr(action, "content", "")
        reward_score = grade_task(task_type, result)
        reward = reward_score

        self.history.append(self.current_email.email)

        if action.action_type == "reply":
            self.tasks = []
        elif action.action_type == "schedule":
            self.calendar.append("New meeting scheduled")
        elif action.action_type == "ignore":
            pass

        next_email = self.generate_email()
        self.tasks = extract_tasks_from_email(next_email)

        self.current_email = Observation(
            email=next_email,
            sender="boss@company.com",
            subject="Follow-up",
            history=self.history,
            current_tasks=self.tasks,
            calendar=self.calendar
        )

        self.done = False
        return self.current_email, reward, self.done, {}

    def state(self):
        return self.current_email

    def calculate_reward(self, action: Action):
        score = 0.10  # start above 0.0
        reason = ""

        for task in self.tasks:
            if "meeting" in task and "meeting" in action.content.lower():
                score += 0.2
                reason += "Understood meeting. "

            if "report" in task and "report" in action.content.lower():
                score += 0.2
                reason += "Understood report. "

        if self.priority == "high":
            if "asap" in action.content.lower():
                score += 0.2
                reason += "Handled urgency. "

        if self.check_conflict(self.current_email.email):
            if "reschedule" in action.content.lower():
                score += 0.2
                reason += "Resolved conflict. "

        if action.action_type == "reply":
            score += 0.2
            reason += "Replied correctly. "

        if len(self.history) > 0:
            if "report" in self.history[-1].lower() and "report" in action.content.lower():
                score += 0.1
                reason += "Used memory. "

        if score <= 0.10:
            reason = "Poor response."

        if len(self.tasks) > 2:
            score += 0.2
            reason += "Handled multiple tasks."

        # clamp strictly between 0 and 1
        score = max(0.01, min(0.99, score))
        return Reward(score=score, reason=reason)

    

