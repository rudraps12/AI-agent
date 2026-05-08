todos = []


def add_tasks(task_list, priority):

    for task in task_list:

        todos.append({
            "task": task,
            "priority": priority,
            "status": "pending"
        })


def get_tasks():
    return todos


def clear_tasks():
    todos.clear()


def show_tasks():

    print("\n========== TODO LIST ==========")

    if not todos:
        print("No tasks available.")

    for index, todo in enumerate(todos):

        print(
            f"{index + 1}. "
            f"{todo['task']} | "
            f"Priority: {todo['priority']} | "
            f"Status: {todo['status']}"
        )

    print("================================\n")