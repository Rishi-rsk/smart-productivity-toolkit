import os
import datetime
import json

FILE_NAME = "tasks.json"


class Task:
    def __init__(self, task_id, description, priority="normal",
                 completed=False, created_at=None, completed_at=None):
        self.task_id = task_id
        self.description = description
        self.priority = priority
        self.completed = completed
        self.created_at = created_at or datetime.datetime.now().strftime("%d %b %Y, %I:%M %p")
        self.completed_at = completed_at

    def mark_done(self):
        self.completed = True
        self.completed_at = datetime.datetime.now().strftime("%d %b %Y, %I:%M %p")

    def to_dict(self):
        return {
            "id": self.task_id,
            "description": self.description,
            "priority": self.priority,
            "completed": self.completed,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
        }

    @staticmethod
    def from_dict(data):
        return Task(
            data["id"],
            data["description"],
            data["priority"],
            data["completed"],
            data["created_at"],
            data["completed_at"]
        )


class ToDoList:
    def __init__(self):
        self.tasks = {}
        self._id_counter = 1
        self.load_tasks()

    def add_task(self, description, priority="normal"):
        task = Task(self._id_counter, description, priority)
        self.tasks[self._id_counter] = task
        self._id_counter += 1
        self.save_tasks()
        return task

    def complete_task(self, task_id):
        task = self.tasks.get(task_id)
        if task is None:
            return None, "Task not found."
        if task.completed:
            return task, "already_done"
        task.mark_done()
        self.save_tasks()
        return task, "ok"

    def delete_task(self, task_id):
        removed = self.tasks.pop(task_id, None)
        self.save_tasks()
        return removed

    def get_pending(self):
        return [t for t in self.tasks.values() if not t.completed]

    def get_completed(self):
        return [t for t in self.tasks.values() if t.completed]

    def all_tasks(self):
        return list(self.tasks.values())

    # 🔥 NEW: Save tasks
    def save_tasks(self):
        data = [task.to_dict() for task in self.tasks.values()]
        with open(FILE_NAME, "w") as file:
            json.dump(data, file, indent=4)

    # 🔥 NEW: Load tasks
    def load_tasks(self):
        if not os.path.exists(FILE_NAME):
            return
        with open(FILE_NAME, "r") as file:
            data = json.load(file)
            for item in data:
                task = Task.from_dict(item)
                self.tasks[task.task_id] = task
                self._id_counter = max(self._id_counter, task.task_id + 1)


# ── helpers ──────────────────────────────────────────────────────────────────

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def divider(char="─", width=54):
    print(char * width)


def header():
    clear()
    divider("═")
    print("          ✅  MY TO-DO LIST  ✅")
    divider("═")


PRIORITY_COLORS = {"high": "🔴", "normal": "🟡", "low": "🟢"}


def display_task(task):
    status = "✔" if task.completed else "○"
    icon = PRIORITY_COLORS.get(task.priority, "🟡")
    desc = task.description
    if task.completed:
        desc = f"\033[9m{desc}\033[0m"
    print(f"  [{task.task_id}] {status} {icon}  {desc}")
    print(f"        Added  : {task.created_at}")
    if task.completed and task.completed_at:
        print(f"        Done   : {task.completed_at}")


def show_all(todo):
    header()
    if not todo.all_tasks():
        print("\n  No tasks yet. Add one to get started!\n")
        return

    pending = todo.get_pending()
    done = todo.get_completed()

    if pending:
        print(f"\n  PENDING  ({len(pending)})")
        divider()
        for task in pending:
            display_task(task)
            print()

    if done:
        print(f"\n  COMPLETED  ({len(done)})")
        divider()
        for task in done:
            display_task(task)
            print()

    divider()
    print(f"  Total: {len(todo.all_tasks())}  |  Done: {len(done)}  |  Pending: {len(pending)}")


def pick_priority():
    print("\n  Priority:")
    print("    1. High 🔴")
    print("    2. Normal 🟡  (default)")
    print("    3. Low  🟢")
    choice = input("\n  Enter choice (1/2/3): ").strip()
    mapping = {"1": "high", "2": "normal", "3": "low"}
    return mapping.get(choice, "normal")


# ── menu actions ──────────────────────────────────────────────────────────────

def action_add(todo):
    header()
    print("\n  ADD A NEW TASK\n")
    desc = input("  Task description: ").strip()
    if not desc:
        input("\n  ⚠  Description cannot be empty. Press Enter to go back.")
        return
    priority = pick_priority()
    task = todo.add_task(desc, priority)
    print(f"\n  ✅  Task #{task.task_id} added successfully!")
    input("  Press Enter to continue.")


def action_complete(todo):
    header()
    print("\n  MARK TASK AS COMPLETED\n")
    pending = todo.get_pending()
    if not pending:
        input("  No pending tasks right now. Press Enter to go back.")
        return
    for task in pending:
        display_task(task)
        print()
    try:
        task_id = int(input("  Enter task ID to mark done: ").strip())
    except ValueError:
        input("  ⚠  Invalid ID. Press Enter to go back.")
        return
    task, status = todo.complete_task(task_id)
    if status == "ok":
        print(f"\n  ✔  \"{task.description}\" marked as completed!")
    elif status == "already_done":
        print(f"\n  ℹ  Task #{task_id} was already completed.")
    else:
        print(f"\n  ⚠  Task #{task_id} not found.")
    input("  Press Enter to continue.")


def action_delete(todo):
    header()
    print("\n  DELETE A TASK\n")
    if not todo.all_tasks():
        input("  Nothing to delete. Press Enter to go back.")
        return
    for task in todo.all_tasks():
        display_task(task)
        print()
    try:
        task_id = int(input("  Enter task ID to delete: ").strip())
    except ValueError:
        input("  ⚠  Invalid ID. Press Enter to go back.")
        return
    confirm = input(f"  Are you sure you want to delete task #{task_id}? (y/n): ").strip().lower()
    if confirm != "y":
        input("  Cancelled. Press Enter to go back.")
        return
    removed = todo.delete_task(task_id)
    if removed:
        print(f"\n  🗑  \"{removed.description}\" deleted.")
    else:
        print(f"\n  ⚠  Task #{task_id} not found.")
    input("  Press Enter to continue.")


def action_view_pending(todo):
    header()
    print("\n  PENDING TASKS\n")
    pending = todo.get_pending()
    if not pending:
        print("  🎉  All caught up! No pending tasks.")
    else:
        for task in pending:
            display_task(task)
            print()
    divider()
    input("  Press Enter to go back.")


# ── main loop ─────────────────────────────────────────────────────────────────

def main():
    todo = ToDoList()

    while True:
        show_all(todo)
        print("\n  MENU")
        divider()
        print("  1.  Add task")
        print("  2.  Mark task as completed")
        print("  3.  Delete task")
        print("  4.  View pending only")
        print("  5.  Quit")
        divider()
        choice = input("  Choose an option (1-5): ").strip()

        if choice == "1":
            action_add(todo)
        elif choice == "2":
            action_complete(todo)
        elif choice == "3":
            action_delete(todo)
        elif choice == "4":
            action_view_pending(todo)
        elif choice == "5":
            header()
            print("\n  See you later! Keep crushing those tasks. 👋\n")
            divider("═")
            break
        else:
            input("  ⚠  Invalid choice. Press Enter to try again.")


if __name__ == "__main__":
    main()