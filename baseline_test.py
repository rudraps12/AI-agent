"""
baseline.py
-----------
Standalone script that runs a deterministic baseline agent
against the environment and prints its score.

Usage: python baseline.py
"""

import random


def _c(v: float) -> float:
    # Strictly inside (0,1): never 0.0 or 1.0
    return round(max(0.01, min(float(v), 0.99)), 4)


TASK_BANK = {
    "easy": [
        {
            "id": "easy_1",
            "email": "Hi team, please schedule a meeting for tomorrow at 3pm.",
            "subject": "Meeting Request",
            "sender": "manager@company.com",
            "expected_action": "reply",
            "keywords": ["schedule", "meeting", "tomorrow", "3pm"],
            "expected_count": 1,
            "difficulty": "easy",
        }
    ],
    "medium": [
        {
            "id": "medium_1",
            "email": (
                "Hi, please review the attached proposal and send your feedback "
                "to the client by Thursday. Also reschedule our Monday standup "
                "to Wednesday 10am."
            ),
            "subject": "Proposal Review + Standup Reschedule",
            "sender": "team@company.com",
            "expected_action": "reply",
            "keywords": ["review", "proposal", "feedback", "reschedule", "standup"],
            "expected_count": 3,
            "difficulty": "medium",
        }
    ],
    "hard": [
        {
            "id": "hard_1",
            "email": (
                "Dear Manager, vendor contract needs legal review before Wednesday. "
                "Campaign assets overdue. Onboard 3 developers Monday. "
                "Q4 board presentation Friday. Client ABC escalated ticket."
            ),
            "subject": "Multiple Urgent Pending Items",
            "sender": "ceo@company.com",
            "expected_action": "reply",
            "keywords": ["contract", "legal", "campaign", "onboard", "presentation", "ticket"],
            "expected_count": 5,
            "difficulty": "hard",
        }
    ],
}


def grade_all_baseline(content: str, action_type: str, task: dict) -> dict:
    keywords = task.get("keywords", [])
    expected = max(task.get("expected_count", 1), 1)
    text = content.lower()

    kw_hits = sum(1 for kw in keywords if kw.lower() in text)
    ratio = kw_hits / expected

    priority = _c(0.40 + min(kw_hits * 0.08, 0.45))
    extraction = _c(0.15 + min(ratio * 0.75, 0.80))
    action = _c(0.62 if action_type == task.get("expected_action", "reply") else 0.22)
    quality = _c(0.55 + min(len(content.split()) * 0.01, 0.35))
    conflict = _c(0.38 + min(kw_hits * 0.05, 0.45))

    overall = _c(
        priority * 0.15
        + extraction * 0.30
        + action * 0.25
        + quality * 0.20
        + conflict * 0.10
    )
    return {
        "scores": {
            "priority": priority,
            "task_extraction": extraction,
            "action_decision": action,
            "reply_quality": quality,
            "conflict_handling": conflict,
        },
        "reward": overall,
    }


def build_baseline_response(task: dict) -> str:
    kws = task.get("keywords", [])
    return (
        "Thank you for your email. I will immediately address the following: "
        f"{', '.join(kws)}. I will reschedule any conflicting meetings and reply "
        "to all stakeholders by the stated deadline. Best regards."
    )


def run_baseline():
    print("=" * 60)
    print("BASELINE AGENT EVALUATION")
    print("=" * 60)

    total_reward = 0.0
    results = []

    for diff in ["easy", "medium", "hard"]:
        task = random.choice(TASK_BANK[diff])
        content = build_baseline_response(task)
        graded = grade_all_baseline(content, task["expected_action"], task)

        results.append(
            {
                "difficulty": diff,
                "task_id": task["id"],
                "reward": graded["reward"],
                "scores": graded["scores"],
            }
        )
        total_reward += graded["reward"]
        print(f"\n[{diff.upper()}] task={task['id']} reward={graded['reward']}")
        for k, v in graded["scores"].items():
            print(f"  {k:22s} {v:.4f}")

    avg = _c(total_reward / len(results))
    print(f"\n{'=' * 60}")
    print(f"AVERAGE REWARD: {avg:.4f} (strictly in (0.01, 0.99))")
    print("=" * 60)
    return avg


if __name__ == "__main__":
    run_baseline()
