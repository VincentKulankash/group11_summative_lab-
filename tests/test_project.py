from models.project import Project


def test_create_project():
    project = Project(
        "RPG Game",
        "Build an RPG simulator",
        "2026-10-01",
        1
    )

    assert project.id is not None
    assert project.title == "RPG Game"
    assert project.description == "Build an RPG simulator"
    assert project.due_date == "2026-10-01"
    assert project.owner_id == 1
    assert project.task_ids == []


def test_title_setter():
    project = Project("Old Title", "Description", "2026-10-01", 1)

    project.title = "New Title"

    assert project.title == "New Title"


def test_description_setter():
    project = Project("Project", "Old description", "2026-10-01", 1)

    project.description = "New description"

    assert project.description == "New description"


def test_due_date_setter():
    project = Project("Project", "Description", "2026-10-01", 1)

    project.due_date = "2026-12-01"

    assert project.due_date == "2026-12-01"


def test_add_task():
    project = Project("Project", "Description", "2026-10-01", 1)

    result = project.add_task(10)

    assert result is True
    assert project.task_ids == [10]


def test_duplicate_task():
    project = Project("Project", "Description", "2026-10-01", 1)

    project.add_task(10)
    result = project.add_task(10)

    assert result is False
    assert project.task_ids == [10]


def test_remove_task():
    project = Project("Project", "Description", "2026-10-01", 1)

    project.add_task(10)
    result = project.remove_task(10)

    assert result is True
    assert project.task_ids == []


def test_has_task():
    project = Project("Project", "Description", "2026-10-01", 1)

    project.add_task(10)

    assert project.has_task(10) is True
    assert project.has_task(20) is False


def test_task_count():
    project = Project("Project", "Description", "2026-10-01", 1)

    project.add_task(10)
    project.add_task(20)

    assert project.task_count() == 2


def test_clear_tasks():
    project = Project("Project", "Description", "2026-10-01", 1)

    project.add_task(10)
    project.add_task(20)

    project.clear_tasks()

    assert project.task_ids == []


def test_to_dict():
    project = Project(
        "RPG Game",
        "Build an RPG simulator",
        "2026-10-01",
        1
    )

    project.add_task(10)

    data = project.to_dict()

    assert data["id"] == project.id
    assert data["title"] == "RPG Game"
    assert data["description"] == "Build an RPG simulator"
    assert data["due_date"] == "2026-10-01"
    assert data["owner_id"] == 1
    assert data["task_ids"] == [10]


def test_from_dict():
    data = {
        "id": 5,
        "title": "RPG Game",
        "description": "Build an RPG simulator",
        "due_date": "2026-10-01",
        "owner_id": 1,
        "task_ids": [10, 20]
    }

    project = Project.from_dict(data)

    assert project.id == 5
    assert project.title == "RPG Game"
    assert project.description == "Build an RPG simulator"
    assert project.due_date == "2026-10-01"
    assert project.owner_id == 1
    assert project.task_ids == [10, 20]


def test_string_representation():
    project = Project("RPG Game", "Description", "2026-10-01", 1)

    assert str(project) == f"Project #{project.id}: RPG Game"


def test_repr():
    project = Project("RPG Game", "Description", "2026-10-01", 1)

    result = repr(project)

    assert "Project(" in result
    assert "RPG Game" in result