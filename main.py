"""TaskFlow CLI entry point. Owner: YOU."""
import argparse

from utils.storage import Storage
from utils import display
from utils.auth import CURRENT_USER, login_required
from models.user import User
from models.project import Project
from models.task import Task

storage = Storage()

def register():
    """Create a new user account"""
    users = storage.load('users.json', User)

    name = display.ask('Name: ')
    email = display.ask('Email: ')
    password = display.ask('Password: ')

    if not name or not email or not password:
        display.error('All fields are required')
        return 

    if any(u.email == email for u in users):
        display.error('Email already exists')
        return

    users.append(User(name, email, password))
    storage.save('users.json', users)
    display.success(f"Registered {name}.")


def logout():
    CURRENT_USER['user'] = None
    display.success('Logged out.')

@login_required
def add_project():
    """Create a new quest (project) owned by the current user"""
    projects = storage.load('projects.json', Project)
    user = CURRENT_USER['user']

    title = display.ask('Quest title: ')
    description = display.ask('Description: ')
    due_date = display.ask('Due date (YYYY-MM-DD): ')
    difficulty = display.ask('Difficulty (easy/medium/hard/legendary): ')

    if difficulty not in {'easy', 'medium', 'hard', 'legendary'}:
        display.error('Invalid difficulty')
        return

    project = Project(title, description, due_date,user.id, difficulty)
    projects.append(project)
    user.add_project(project.id)

    users = storage.load('users.json', User)
    for i, u in enumerate(users):
        if u.id == user.id:
            users[i] = user
            break

    storage.save('users.json', users)

    storage.save('projects.json', projects)
    display.success('Quest created: {project}')

@login_required
def list_projects():
    """List the current users quest"""
    projects = storage.load('projects.json', Project)
    user = CURRENT_USER['user']

    mine = [p for p in projects if p.owner_id == user.id]

    if not mine:
        display.error('You have no quests yet.')
        return 

    rows = [[p.id, p.title, p.due_date, p.difficulty] for p in mine]
    display.print_table("Your Quests",
                        ["ID", "Title", "Due", "Difficulty"],
                        rows)

@login_required
def add_task():
    tasks = storage.load("tasks.json", Task)

    title = display.ask("Bounty title: ")
    project_id = display.ask("Quest ID: ")

    try:
        project_id = int(project_id)
    except ValueError:
        display.error("Quest ID must be a number.")
        return

    task = Task(title, project_id, assigned_to=CURRENT_USER["user"].id)
    tasks.append(task)
    storage.save("tasks.json", tasks)
    display.success(f"Bounty added: {task}")

@login_required
def complete_task():
    """Mark a bounty as completed."""
    tasks = storage.load("tasks.json", Task)

    task_id = display.ask("Bounty ID: ")

    try:
        task_id = int(task_id)
    except ValueError:
        display.error("ID must be a number.")
        return

    task = next((t for t in tasks if t.id == task_id), None)
    if task is None:
        display.error("Bounty not found.")
        return

    task.complete()
    storage.save("tasks.json", tasks)
    display.success(f"Completed: {task}")
    

@login_required
def list_users():
    """Admin: list all registered users."""
    if CURRENT_USER["user"].role() != "admin":
        display.error("Admin access required.")
        return

    users = storage.load("users.json", User)
    rows = [[u.id, u.name, u.email, u.role()] for u in users]
    display.print_table("Guild Members",
                        ["ID", "Name", "Email", "Role"],
                        rows)

    
MENU = """Guild manager
        1. Create quest
        2. List my quests
        3. Add bounty
        4. Complete bounty
        5. List all members (admin)
        6. Logout 
        0. Exit
        """

def menu_loop():
    
    while True:
        print(MENU)
        choice = display.ask('Choose: ')

        if choice == '1':
            add_project()
        elif choice == '2':
            list_projects()
        elif choice == '3':
            add_task()
        elif choice == '4':
            complete_task()
        elif choice == '5':
            list_users()
        elif choice == '6':
            logout()
        elif choice == '0':
            display.success('Farewell, adventurer.')
            return
        else:
            display.error('Invalid choice.')



def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="guild-manager",
        description="Guild Manager — a CLI project management tool.",
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("register", help="Register a new user")
    sub.add_parser("login", help="Log in")
    sub.add_parser("menu", help="Open the interactive menu")
    sub.add_parser("list-users", help="List all users (admin)")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "register":
        register()
    elif args.command == "login":
        login()
    elif args.command == "menu":
        if CURRENT_USER["user"] is None:
            display.error("Log in first.")
            return
        menu_loop()
    elif args.command == "list-users":
        list_users()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()