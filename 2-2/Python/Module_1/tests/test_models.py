import unittest
from Module_1.models.user import User


class TestUserModel(unittest.TestCase):

    def setUp(self):
        User.use_db("test")  # Працюємо з тестовою БД
        self.user = User.create(name="TestUser", email="test@example.com")

    def test_create_user(self):
        self.assertIsNotNone(self.user)
        self.assertEqual(self.user["name"], "TestUser")

    def test_get_user(self):
        fetched = User.get(self.user["id"])
        self.assertEqual(fetched["email"], "test@example.com")

    def test_update_user(self):
        updated = User.update(self.user["id"], name="UpdatedUser")
        self.assertEqual(updated["name"], "UpdatedUser")

    def test_delete_user(self):
        result = User.delete(self.user["id"])
        self.assertTrue(result)
        self.assertIsNone(User.get(self.user["id"]))


if __name__ == '__main__':
    unittest.main()
