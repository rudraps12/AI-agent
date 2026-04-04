import requests

URL = "http://127.0.0.1:8000/process"

test_emails = [
    "URGENT: submit report and call manager",
    "Please call the client tomorrow",
    "Reminder to submit your assignment",
    "Hello, how are you?",
    "Schedule a meeting with the team",
]


def test_api():
    print("\n===== BASELINE TEST START =====\n")

    for i, email in enumerate(test_emails, 1):
        payload = {
            "email_text": email
        }

        try:
            response = requests.post(URL, json=payload)

            print(f"\nTest Case {i}")
            print("Input Email:", email)

            if response.status_code == 200:
                data = response.json()

                print("Task Type:", data.get("task_type"))
                print("Tasks:", data.get("tasks"))
                print("Reward:", data.get("reward"))
            else:
                print("Error:", response.text)

        except Exception as e:
            print("Exception:", str(e))

    print("\n===== TEST COMPLETE =====\n")


if __name__ == "__main__":
    test_api()