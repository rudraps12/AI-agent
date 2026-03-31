def grade(action, task):
    score = 0.0

    content = action.content.lower()

    # Check action type
    if action.action_type == task["expected_action"]:
        score += 0.3

    # Check keywords
    matched = 0
    for word in task["expected_keywords"]:
        if word in content:
            matched += 1

    score += 0.7 * (matched / len(task["expected_keywords"]))

    return round(score, 2)