# Guild Manager CLI

A command-line project management tool with a guild/adventure theme, built in Python with object-oriented design, JSON persistence, role-based access, and unit tests.

Guildmasters create **Quests** and post **Bounties**. Adventurers browse open quests, accept bounties on a first-come-first-served basis, and mark them complete.

---

## Features

- **User registration and login** with bcrypt-hashed passwords
- **Role-based access** — Guildmasters and Adventurers see different menus
- **Quests and Bounties** — quests contain bounties; bounties are individual jobs
- **First-come, first-served bounty acceptance**
- **JSON persistence** — data survives between runs
- **Input validation** — no past due dates, no invalid difficulty, no duplicate emails
- **Rich CLI output** — formatted tables and colored status messages
- **Unit tests** — 39+ tests covering models and auth

---

## Roles

| Role | Internal value | What they can do |
|---|---|---|
| **Guildmaster** | `admin` | Create quests, add bounties, list all quests, list all members |
| **Adventurer** | `user` | Browse open quests, accept bounties, view personal bounties, complete bounties |

Role is selected at registration. The CLI shows a different menu depending on which role you log in as.

---


---

## Setup

### Prerequisites

- Python 3.10 or higher
- Git

### Clone the repository

```bash
git clone https://github.com/VincentKulankash/group11_summative_lab-.git
cd group11_summative_lab-

pip install pipenv
pipenv install
pipenv shell

The CLI has two commands: register and login.

python3 main.py register

You'll be prompted for:

Name

Email

Password

Role (admin for Guildmaster, user for Adventurer; default is user)

#Login to the system
python3 main.py login


pytest -v