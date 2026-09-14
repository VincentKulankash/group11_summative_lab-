import unittest

from models.task import Task, VALID_STATUSES


class TestTask(unittest.TestCase):

    # ---------- creation ----------

    def test_task_creation_defaults(self):
        task = Task("Defeat the dragon", project_id=1)
        self.assertEqual(task.title, "Defeat the dragon")
        self.assertEqual(task.project_id, 1)
        self.assertEqual(task.status, "todo")
        self.assertIsNone(task.assigned_to)

    def test_task_creation_with_all_fields(self):
        task = Task("Defeat the dragon", project_id=1,
                    assigned_to=42, status="in-progress")
        self.assertEqual(task.title, "Defeat the dragon")
        self.assertEqual(task.project_id, 1)
        self.assertEqual(task.assigned_to, 42)
        self.assertEqual(task.status, "in-progress")

    def test_ids_are_auto_incremented(self):
        t1 = Task("First", project_id=1)
        t2 = Task("Second", project_id=1)
        self.assertEqual(t2.id, t1.id + 1)

    # ---------- status ----------

    def test_invalid_status_raises_on_creation(self):
        with self.assertRaises(ValueError):
            Task("Bad", project_id=1, status="nonsense")

    def test_invalid_status_raises_on_setter(self):
        task = Task("Ok", project_id=1)
        with self.assertRaises(ValueError):
            task.status = "nonsense"

    def test_valid_status_can_be_set(self):
        task = Task("Ok", project_id=1)
        task.status = "in-progress"
        self.assertEqual(task.status, "in-progress")

    # ---------- complete ----------

    def test_complete(self):
        task = Task("Defeat the dragon", project_id=1)
        task.complete()
        self.assertEqual(task.status, "done")

    # ---------- serialization ----------

    def test_to_dict(self):
        task = Task("Defeat the dragon", project_id=1,
                    assigned_to=42, status="in-progress")
        self.assertEqual(task.to_dict(), {
            "id": task.id,
            "title": "Defeat the dragon",
            "status": "in-progress",
            "project_id": 1,
            "assigned_to": 42,
        })

    def test_from_dict(self):
        data = {
            "id": 7,
            "title": "Defeat the dragon",
            "status": "done",
            "project_id": 1,
            "assigned_to": 42,
        }
        task = Task.from_dict(data)
        self.assertEqual(task.id, 7)
        self.assertEqual(task.title, "Defeat the dragon")
        self.assertEqual(task.status, "done")
        self.assertEqual(task.project_id, 1)
        self.assertEqual(task.assigned_to, 42)

    def test_round_trip(self):
        original = Task("Defeat the dragon", project_id=1,
                        assigned_to=42, status="in-progress")
        saved = original.to_dict()
        restored = Task.from_dict(saved)
        self.assertEqual(restored.to_dict(), saved)

    # ---------- __str__ ----------

    def test_str(self):
        task = Task("Defeat the dragon", project_id=1, task_id=5)
        self.assertIn("Task #5", str(task))
        self.assertIn("[todo]", str(task))
        self.assertIn("Defeat the dragon", str(task))


if __name__ == "__main__":
    unittest.main()