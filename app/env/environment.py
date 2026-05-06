import random
from app.models.observation import Observation
from app.models.action import Action
import re
from datetime import datetime
from app.models.reward import Reward, grade_task


def get_task_type(email_text):
    if "urgent" in email_text.lower():
        return "priority"
    elif "call" in email_text.lower() or "submit" in email_text.lower():
        return "task_extraction"
    else:
        return "action_decision"
    
def grade_task(task_type, output):
    if task_type == "task_extraction":
        return 1.0 if output else 0.3

    elif task_type == "priority":
        return 1.0 if output in ["HIGH", "MEDIUM", "LOW"] else 0.2

    elif task_type == "action_decision":
        return 1.0 if output in ["reply", "escalate", "ignore"] else 0.2

    return 0.0
def extract_tasks_from_email(email_text):
    tasks = []

    text = email_text.lower()

    sentences = re.split(r'[.!?\\n]', text)

    action_words = [
        "send",
        "submit",
        "prepare",
        "update",
        "complete",
        "finish",
        "review",
        "create",
        "attend",
        "write",
        "solve",
        "schedule",
        "call",
        "reply"
    ]

    ignore_words = [
        "you are informed",
        "kindly ensure",
        "all questions are",
        "the assignment is"
    ]

    for sentence in sentences:
        sentence = sentence.strip()

        if not sentence:
            continue

        if sentence.startswith((
            "hi",
            "hello",
            "thanks",
            "regards"
        )):
            continue

        if any(
            phrase in sentence
            for phrase in ignore_words
        ):
            continue

        for word in action_words:
            if word in sentence:
                cleaned = (
                    sentence
                    .replace("please", "")
                    .replace("kindly", "")
                    .replace("also", "")
                    .strip()
                )

                if cleaned not in tasks:
                    tasks.append(cleaned)

                break

    if "deadline" in text:
        tasks.append("complete before deadline")

    if "asap" in text or "urgent" in text:
        tasks.append("handle urgently")

    return tasks


class EmailEnv:

    # INIT
    def __init__(self):
        self.current_email = None
        self.done = False
        self.history = []
        self.tasks = []
        self.calendar = []
        self.priority = "low"

    # EMAIL GENERATOR
    def generate_email(self):
        emails = [
            "Urgent: attend meeting at 5 PM and send report ASAP",
            "Reminder to send report before deadline",
            "Can we reschedule the meeting to 6 PM?",
            "Please schedule a meeting and prepare report",
            "ASAP: finish the report and attend meeting"
        ]
        return random.choice(emails)


    #  PRIORITY DETECTION
    def detect_priority(self, email: str):
        email_lower = email.lower()

        if any(
            w in email_lower
            for w in (
                "urgent",
                "asap",
                "as soon as",
                "immediately",
                "immediate",
                "critical",
                "eod today",
            )
        ):
            return "high"

        if any(
            w in email_lower
            for w in (
                "soon",
                "priority",
                "important",
                "by tomorrow",
                "end of week",
            )
        ):
            return "medium"

        # DATE DETECTION (e.g. "3 April 2026")
        date_match = re.search(r"(\d{1,2}\s+[a-zA-Z]+\s+\d{4})", email)

        if date_match:
            try:
                deadline_str = date_match.group()
                deadline_date = datetime.strptime(deadline_str, "%d %B %Y")
                today = datetime.today()
                diff = (deadline_date - today).days

                if diff <= 2:
                    return "high"
                if diff <= 5:
                    return "medium"
                return "low"

            except Exception:
                pass

        return "low"

    #  CONFLICT DETECTION
    def check_conflict(self, email: str):
        if "5 pm" in email.lower():
            for event in self.calendar:
                if "5 PM" in event:
                    return True
        return False

    #  RESET
    def reset(self, email_text=None):

        if email_text is None:
            email_text = self.generate_email()

        self.tasks = extract_tasks_from_email(
            email_text
        )

        self.priority = self.detect_priority(
            email_text
        )

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

    #  STEP
    def step(self, action: Action):
    # Get task type
        task_type = get_task_type(self.current_email.email)

    # Safe access
        result = getattr(action, "content", "")

    # Calculate reward
        reward_score = grade_task(task_type, result)
        reward = Reward(
            score=float(reward_score),
            reason=f"task_type={task_type}",
        )

    # Save history
        self.history.append(self.current_email.email)

    # Handle actions
        if action.action_type == "reply":
            self.tasks = []

        elif action.action_type == "schedule":
            self.calendar.append("New meeting scheduled")

        elif action.action_type == "ignore":
            pass

    # Generate next email
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

    #  STATE
    def state(self):
        return self.current_email

    #   REWARD FUNCTION
    def calculate_reward(self, action: Action):
        score = 0.0
        reason = ""

        # Task understanding
        for task in self.tasks:
            if "meeting" in task and "meeting" in action.content.lower():
                score += 0.2
                reason += "Understood meeting. "

            if "report" in task and "report" in action.content.lower():
                score += 0.2
                reason += "Understood report. "

        # Priority
        if self.priority == "high":
            if "asap" in action.content.lower():
                score += 0.2
                reason += "Handled urgency. "

        # Conflict
        if self.check_conflict(self.current_email.email):
            if "reschedule" in action.content.lower():
                score += 0.2
                reason += "Resolved conflict. "

        # Action
        if action.action_type == "reply":
            score += 0.2
            reason += "Replied correctly. "

        # Memory bonus
        if len(self.history) > 0:
            if "report" in self.history[-1].lower() and "report" in action.content.lower():
                score += 0.1
                reason += "Used memory. "

        if score == 0:
            reason = "Poor response."
        
        if len(self.tasks)>2:
            score += 0.2
            reason +="handled multiple tasks."

        return Reward(score=score, reason=reason)
    
    def process_real_email(env, email_text):
        env.reset(email_text)

        return {
            "tasks": env.tasks,
            "priority": env.priority
        }

def process_real_email(env, email_text):

    env.reset(email_text)

    return {
        "tasks": env.tasks,
        "priority": env.priority
    }