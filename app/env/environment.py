import random
from app.models.observation import Observation
from app.models.action import Action
from app.models.reward import Reward


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

    #  TASK EXTRACTION
    def extract_tasks(self, email: str):
        tasks = []
        email_lower = email.lower()

        keywords = {
            "meeting": "attend meeting",
            "report": "send report",
            "schedule": "schedule event",
            "reschedule": "reschedule meeting",
            "deadline": "complete before deadline",
            "asap": "urgent task",
            "reminder": "follow up"
        }

        for key, value in keywords.items():
            if key in email_lower:
                tasks.append(value)

        return list(set(tasks))

    #  PRIORITY DETECTION
    def detect_priority(self, email: str):
        email_lower = email.lower()

        if "urgent" in email_lower or "asap" in email_lower:
            return "high"
        elif "soon" in email_lower:
            return "medium"
        else:
            return "low"

    #  CONFLICT DETECTION
    def check_conflict(self, email: str):
        if "5 pm" in email.lower():
            for event in self.calendar:
                if "5 PM" in event:
                    return True
        return False

    #  RESET
    def reset(self):
        email_text = self.generate_email()

        self.tasks = self.extract_tasks(email_text)
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

    #  STEP
    def step(self, action: Action):
        reward = self.calculate_reward(action)

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
        self.tasks = self.extract_tasks(next_email)

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

    #  REWARD FUNCTION
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

        return Reward(score=score, reason=reason)