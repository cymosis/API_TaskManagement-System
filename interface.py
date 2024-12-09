##importng the classes and subclasses
from task import PersonalTask, WorkTask
from task_manager import TaskManager


###create the interface
def main():
    manager = TaskManager()
    while True:
        print("\nTask Management System")
        print("1. Create Task")
        print("2. View Tasks")
        print("3. Delete Task")
        print("4. Save Tasks to File")
        print("5. Load Tasks from File")
        print("6. View Pending Tasks")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            task_type = input("Enter task type (personal/work): ").strip().lower()
            title = input("Enter title: ")
            due_date = input("Enter due date (YYYY-MM-DD): ")
            description = input("Enter description (optional): ")

            if task_type == "personal":
                priority = input("Enter priority (low/medium/high): ").strip().lower()
                task = PersonalTask(title, due_date, description, priority)
            elif task_type == "work":
                task = WorkTask(title, due_date, description)
                team_member = input("Enter a team member (or leave blank): ").strip()
                if team_member:
                    task.add_team_member(team_member)
            else:
                print("Invalid task type.")
                continue

            manager.add_task(task)

        elif choice == "2":
            manager.list_tasks()

        elif choice == "3":
            task_id = int(input("Enter task ID to delete: "))
            manager.delete_task(task_id)

        elif choice == "4":
            manager.save_task()

        elif choice == "5":
            manager.load_task()

        elif choice == "6":
            pending_tasks = manager.get_pending_tasks()
            for task in pending_tasks:
                print(task)

        elif choice == "7":
            print("Exiting...")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
