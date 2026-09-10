"""TaskFlow CLI entry point. Owner: YOU."""
import argparse
from utils.storage import Storage
from utils import display
from utils.auth import CURRENT_USER, login_required
from models.user import User
from models.project import Project
from models.task import Task


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="taskflow", description="TaskFlow CLI")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("register", help="Register a new user")
    sub.add_parser("login", help="Login")
    sub.add_parser("menu", help="Open interactive menu")

    # TODO (YOU): add subcommands:
    # list-projects, add-project, add-task, complete-task

    return parser


def main():
    # TODO (YOU): load storage, dispatch on args.command
    print("TaskFlow CLI — scaffold ready.")


if __name__ == "__main__":
    main()