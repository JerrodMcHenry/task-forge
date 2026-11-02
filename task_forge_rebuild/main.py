
from storage import save_tasks, load_tasks
from task_service import create_task, complete_task, delete_task


def main():
    tasks = load_tasks()
    next_task_id = max(tasks.keys(), default=0) + 1

    while True:
        print("\n--- Task Manager ---")
        print("1. Create task")
        print("2. View tasks")
        print("3. Complete task")
        print("4. Delete task")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            title = input("Please enter your task title: ").strip()

            if not title:
                print("Not a valid title. Please try again.")
                continue

            create_task(tasks, next_task_id, title)
            save_tasks(tasks)

            print(f"Task {next_task_id} created successfully.")
            next_task_id += 1

        elif choice == "2":
            if not tasks:
                print("No tasks found")
            else:
                for task in tasks.values():
                    print(
                        f'ID: {task["id"]} | '
                        f'{task["title"]} | '
                        f'{task["status"]}'
                    )

        elif choice == "3":
            try:
                task_id = int(
                    input("Which task would you like to complete?: ")
                )
            except ValueError:
                print("Please enter a valid number.")
                continue

            if complete_task(tasks, task_id):
                save_tasks(tasks)
                print(f"Task {task_id} marked as completed.")
            else:
                print("Task not found")

        elif choice == "4":
            try:
                task_id = int(
                    input("Which task would you like to delete?: ")
                )
            except ValueError:
                print("Please enter a valid task ID")
                continue

            if delete_task(tasks, task_id):
                save_tasks(tasks)
                print(f"Task {task_id} has been deleted successfully")
            else:
                print("Task not found")

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1-5.")


if __name__ == "__main__":
    main()
