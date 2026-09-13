import unittest

from Task import Task, TaskStatus


class TestTask(unittest.TestCase):

    def test_task_creation(self):
        task = Task(
            task_id=1,
            title="Defeat the dragon",
            assigned_user="Hero",
            project="RPG Battle Simulator"
        )

        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Defeat the dragon")
        self.assertEqual(task.status, TaskStatus.TODO)
        self.assertEqual(task.assigned_user, "Hero")
        self.assertEqual(task.project, "RPG Battle Simulator")

    def test_mark_complete(self):
        task = Task(1, "Defeat the dragon")

        task.mark_complete()

        self.assertEqual(task.status, TaskStatus.DONE)

    def test_to_dict(self):
        task = Task(
            1,
            "Defeat the dragon",
            TaskStatus.IN_PROGRESS,
            "Hero",
            "RPG Battle Simulator"
        )

        result = task.to_dict()

        expected = {
            "id": 1,
            "title": "Defeat the dragon",
            "status": "in-progress",
            "assigned_user": "Hero",
            "project": "RPG Battle Simulator",
        }

        self.assertEqual(result, expected)

    def test_from_dict(self):
        data = {
            "id": 1,
            "title": "Defeat the dragon",
            "status": "done",
            "assigned_user": "Hero",
            "project": "RPG Battle Simulator",
        }

        task = Task.from_dict(data)

        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Defeat the dragon")
        self.assertEqual(task.status, TaskStatus.DONE)
        self.assertEqual(task.assigned_user, "Hero")
        self.assertEqual(task.project, "RPG Battle Simulator")

    def test_to_dict_and_from_dict_round_trip(self):
        original = Task(
            1,
            "Defeat the dragon",
            TaskStatus.IN_PROGRESS,
            "Hero",
            "RPG Battle Simulator"
        )

        saved = original.to_dict()
        restored = Task.from_dict(saved)

        self.assertEqual(restored.to_dict(), saved)


if __name__ == "__main__":
    unittest.main()
