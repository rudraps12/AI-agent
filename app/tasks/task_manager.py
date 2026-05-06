from app.services.todo_service import get_tasks


def show_tasks():
    tasks = get_tasks()

    print('\n========== TODO LIST ==========')

    if not tasks:
        print('No tasks available.')

    for index, task in enumerate(tasks):
        print(
            f\"{index + 1}. "
            f\"{task['task']} | "
            f\"Priority: {task['priority']} | "
            f\"Status: {task['status']}\"
        )

    print('===============================\\n')