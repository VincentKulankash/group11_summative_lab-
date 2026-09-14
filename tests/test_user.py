import unittest

from models.user import User


class TestUser(unittest.TestCase):

    def setUp(self):
        self.user = User(
            name="Mohamedamin",
            email="mohamedamin@example.com",
            password="password123"
        )

    def test_user_creation(self):
        self.assertEqual(self.user._name, "Mohamedamin")
        self.assertEqual(self.user._email, "mohamedamin@example.com")
        self.assertEqual(self.user.role(), "user")

    def test_password_check(self):
        self.assertTrue(self.user.check_password("password123"))
        self.assertFalse(self.user.check_password("wrongpassword"))

    def test_add_project(self):
        self.user.add_project(1)
        self.user.add_project(2)

        self.assertEqual(self.user.project_ids, [1, 2])

    def test_project_ids_returns_copy(self):
        self.user.add_project(1)

        project_ids = self.user.project_ids
        project_ids.append(99)

        self.assertEqual(self.user.project_ids, [1])

    def test_to_dict(self):
        self.user.add_project(10)

        data = self.user.to_dict()

        self.assertEqual(data["name"], "Mohamedamin")
        self.assertEqual(data["email"], "mohamedamin@example.com")
        self.assertEqual(data["role"], "user")
        self.assertEqual(data["project_ids"], [10])
        self.assertIn("password_hash", data)

    def test_from_dict(self):
        data = {
            "id": 5,
            "name": "Ali",
            "email": "ali@example.com",
            "password_hash": "hashed_password",
            "role": "admin",
            "project_ids": [1, 2, 3]
        }

        user = User.from_dict(data)

        self.assertEqual(user._id, 5)
        self.assertEqual(user._name, "Ali")
        self.assertEqual(user._email, "ali@example.com")
        self.assertEqual(user._password_hash, "hashed_password")
        self.assertEqual(user.role(), "admin")
        self.assertEqual(user.project_ids, [1, 2, 3])


if __name__ == "__main__":
    unittest.main()