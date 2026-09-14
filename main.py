"""TaskFlow CLI entry point. Owner: YOU."""
import argparse

from utils.storage import Storage
from utils import display
from utils.auth import CURRENT_USER, login_required
from models.user import User
from models.project import Project
from models.task import Task
from datetime import datetime

storage = Storage()

def register():
    """Create a new user account"""
    users = storage.load('users.json', User)

    name = display.ask('Name: ')
    email = display.ask('Email: ')
    password = display.ask('Password: ')
    role = display.ask("Role (admin/user) [user]: ").strip().lower() or "user"

    if role not in {'admin', 'user'}:
        display.error("Role must be 'admin' or 'user'")
        return
    
    if not name or not email or not password:
        display.error('All fields are required')
        return 

    if any(u.email == email for u in users):
        display.error('Email already exists')
        return

    users.append(User(name, email, password, role=role))
    storage.save('users.json', users)
    display.success(f"Registered {name} as {role}.")

def login():
    """Authenticate a user and set CURRENT_USER."""
    users = storage.load("users.json", User)

    email = display.ask("Email: ")
    password = display.ask("Password: ")

    user = next((u for u in users if u.email == email), None)

    if user is None or not user.check_password(password):
        display.error("Invalid email or password.")
        return

    CURRENT_USER["user"] = user
    role_label = "Guild master" if user.role() == "admin" else "Adventurer"
    display.success(f"Logged in as {user.name} ({role_label}).")
    return user


def logout():
    CURRENT_USER['user'] = None
    display.success('Logged out.')


@login_required
def add_project():
    """Create a new quest (admin only)."""
    if CURRENT_USER["user"].role() != "admin":
        display.error("Only guild masters can create quests.")
        return

    projects = storage.load("projects.json", Project)
    user = CURRENT_USER["user"]

    title = display.ask("Quest title: ")
    description = display.ask("Description: ")

    while True:
        due_date = display.ask("Due date (YYYY-MM-DD): ")
        try:
            parsed = datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            display.error("Invalid format. Use YYYY-MM-DD.")
            continue
        if parsed.date() < datetime.today().date():
            display.error("Due date cannot be in the past.")
            continue
        break

    difficulty = display.ask("Difficulty (easy/medium/hard/legendary): ").strip().lower()
    if difficulty not in {"easy", "medium", "hard", "legendary"}:
        display.error("Invalid difficulty.")
        return

    project = Project(title, description, due_date, user.id, difficulty)
    projects.append(project)
    user.add_project(project.id)

    users = storage.load("users.json", User)
    for i, u in enumerate(users):
        if u.id == user.id:
            users[i] = user
            break
    storage.save("users.json", users)
    storage.save("projects.json", projects)
    display.success(f"Quest created: {project}")

@login_required
def list_all_quests():
    """Guild master: see every quest in the guild."""
    if CURRENT_USER["user"].role() != "admin":
        display.error("Only guild masters can view all quests.")
        return

    projects = storage.load("projects.json", Project)

    if not projects:
        display.error("No quests have been created yet.")
        return

    rows = [[p.id, p.title, p.due_date, p.difficulty, p.owner_id] for p in projects]
    display.print_table("All Quests",
                        ["ID", "Title", "Due", "Difficulty", "Owner"],
                        rows)
@login_required
def add_task():
    """Guild master: add a bounty to a quest."""
    if CURRENT_USER["user"].role() != "admin":
        display.error("Only guild masters can create bounties.")
        return

    tasks = storage.load("tasks.json", Task)
    projects = storage.load("projects.json", Project)

    if not projects:
        display.error("Create a quest first.")
        return

    rows = [[p.id, p.title, p.difficulty] for p in projects]
    display.print_table("All Quests",
                        ["ID", "Title", "Difficulty"],
                        rows)

    title = display.ask("Bounty title: ")
    project_id = display.ask("Quest ID: ")

    try:
        project_id = int(project_id)
    except ValueError:
        display.error("Quest ID must be a number.")
        return

    if project_id not in [p.id for p in projects]:
        display.error("Quest not found.")
        return

    task = Task(title, project_id)   # assigned_to stays None
    tasks.append(task)

    for p in projects:
        if p.id == project_id:
            p.add_task(task.id)
            break
    storage.save("projects.json", projects)
    storage.save("tasks.json", tasks)
    display.success(f"Bounty added: {task}")

@login_required
def list_users():
    """Guild master: list all registered users."""
    if CURRENT_USER["user"].role() != "admin":
        display.error("Admin access required.")
        return

    users = storage.load("users.json", User)
    rows = [[u.id, u.name, u.email, u.role()] for u in users]
    display.print_table("Guild Members",
                        ["ID", "Name", "Email", "Role"],
                        rows)
@login_required
def browse_quests():
    """Adventurer: list all quests that still have open bounties."""
    if CURRENT_USER["user"].role() == "admin":
        display.error("Guildmasters don't browse bounties.")
        return

    tasks = storage.load("tasks.json", Task)
    projects = storage.load("projects.json", Project)

    # quests that still have at least one unassigned todo bounty
    open_project_ids = {
        t.project_id for t in tasks
        if t.assigned_to is None and t.status == "todo"
    }

    available = [p for p in projects if p.id in open_project_ids]

    if not available:
        display.error("No quests have open bounties right now.")
        return

    rows = []
    for p in available:
        open_count = sum(
            1 for t in tasks
            if t.project_id == p.id
            and t.assigned_to is None
            and t.status == "todo"
        )
        rows.append([p.id, p.title, p.difficulty, open_count])

    display.print_table("Open Quests",
                        ["ID", "Title", "Difficulty", "Open Bounties"],
                        rows)


@login_required
def accept_bounty():
    """Adventurer: pick a quest, then accept a bounty from it."""
    if CURRENT_USER["user"].role() == "admin":
        display.error("Guild masters don't accept bounties.")
        return

    tasks = storage.load("tasks.json", Task)
    projects = storage.load("projects.json", Project)
    user = CURRENT_USER["user"]

    # show open quests first
    open_project_ids = {
        t.project_id for t in tasks
        if t.assigned_to is None and t.status == "todo"
    }
    available_quests = [p for p in projects if p.id in open_project_ids]

    if not available_quests:
        display.error("No quests have open bounties right now.")
        return

    rows = [[p.id, p.title, p.difficulty] for p in available_quests]
    display.print_table("Open Quests",
                        ["ID", "Title", "Difficulty"],
                        rows)

    # ask which quest
    quest_id = display.ask("Quest ID: ")
    try:
        quest_id = int(quest_id)
    except ValueError:
        display.error("Quest ID must be a number.")
        return

    quest = next((p for p in available_quests if p.id == quest_id), None)
    if quest is None:
        display.error("Quest not found or has no open bounties.")
        return

    # show that quest's open bounties
    open_bounties = [
        t for t in tasks
        if t.project_id == quest.id
        and t.assigned_to is None
        and t.status == "todo"
    ]

    rows = [[t.id, t.title, t.status] for t in open_bounties]
    display.print_table(f"Open Bounties — {quest.title}",
                        ["ID", "Title", "Status"],
                        rows)

    # ask which bounty
    task_id = display.ask("Bounty ID to accept: ")
    try:
        task_id = int(task_id)
    except ValueError:
        display.error("ID must be a number.")
        return

    # re-check the bounty is still available (first come, first served)
    task = next(
        (t for t in tasks
         if t.id == task_id
         and t.project_id == quest.id
         and t.assigned_to is None
         and t.status == "todo"),
        None,
    )
    if task is None:
        display.error("That bounty was just taken or doesn't exist.")
        return

    task.assign_to(user.id)
    storage.save("tasks.json", tasks)
    display.success(f"You accepted: {task}")

@login_required
def my_bounties():
    """Adventurer: show all bounties assigned to them (any status)."""
    if CURRENT_USER["user"].role() == "admin":
        display.error("Guild masters don't have personal bounties.")
        return

    tasks = storage.load("tasks.json", Task)
    projects = storage.load("projects.json", Project)
    user = CURRENT_USER["user"]

    mine = [t for t in tasks if t.assigned_to == user.id]

    if not mine:
        display.error("You haven't accepted any bounties yet.")
        return

    titles = {p.id: p.title for p in projects}
    rows = [[t.id, t.title, titles.get(t.project_id, "—"), t.status] for t in mine]
    display.print_table("My Bounties",
                        ["ID", "Title", "Quest", "Status"],
                        rows)
@login_required
def complete_my_bounty():
    """Adventurer: mark one of their bounties as done."""
    if CURRENT_USER["user"].role() == "admin":
        display.error("Guild masters don't complete bounties.")
        return

    tasks = storage.load("tasks.json", Task)
    user = CURRENT_USER["user"]

    mine = [t for t in tasks if t.assigned_to == user.id and t.status != "done"]

    if not mine:
        display.error("You have no open bounties to complete.")
        return

    rows = [[t.id, t.title, t.status] for t in mine]
    display.print_table("Your Open Bounties",
                        ["ID", "Title", "Status"],
                        rows)

    task_id = display.ask("Bounty ID to complete: ")

    try:
        task_id = int(task_id)
    except ValueError:
        display.error("ID must be a number.")
        return

    task = next((t for t in mine if t.id == task_id), None)
    if task is None:
        display.error("That bounty is not in your open list.")
        return

    task.complete()
    storage.save("tasks.json", tasks)
    display.success(f"Completed: {task}")
    
GUILDMASTER_MENU = """
=== Guild Manager (Guildmaster) ===
1. Create Quest
2. List All Quests
3. Add Bounty
4. List All Members
5. Logout
0. Exit
"""

ADVENTURER_MENU = """
=== Guild Manager (Adventurer) ===
1. Browse Quests
2. Accept a Bounty
3. My Bounties
4. Complete a Bounty
5. Logout
0. Exit
"""


def menu_loop():
    """Show the role-appropriate menu and dispatch."""
    user = CURRENT_USER["user"]

    if user.role() == "admin":
        menu = GUILDMASTER_MENU
    else:
        menu = ADVENTURER_MENU

    while True:
        print(menu)
        choice = display.ask("Choose: ")

        if user.role() == "admin":
            if choice == "1":
                add_project()
            elif choice == "2":
                list_all_quests()
            elif choice == "3":
                add_task()
            elif choice == "4":
                list_users()
            elif choice == "5":
                logout()
                return
            elif choice == "0":
                display.success("Farewell, guild master.")
                return
            else:
                display.error("Invalid choice.")
        else:
            if choice == "1":
                browse_quests()
            elif choice == "2":
                accept_bounty()
            elif choice == "3":
                my_bounties()
            elif choice == "4":
                complete_my_bounty()
            elif choice == "5":
                logout()
                return
            elif choice == "0":
                display.success("Farewell, adventurer.")
                return
            else:
                display.error("Invalid choice.")

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="guild-manager",
        description="Guild Manager — a CLI project management tool.",
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("register", help="Register a new user")
    sub.add_parser("login", help="Log in and open the menu")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "register":
        register()
    elif args.command == "login":
        if login() is not None:
            menu_loop()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()