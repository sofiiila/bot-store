import unittest
from datetime import datetime

from src.db_client.db_client_types import UserDocument, CategoriesEnum


class TestUserDocument(unittest.TestCase):

    def test_good_case_create_model(self):
        """
        Проверяет успешное создание модели пользователя
        """
        user_id = 1
        user_document = UserDocument.create_model(user_id)

        self.assertIsInstance(user_document, UserDocument)

        self.assertEqual(user_document.user_id, user_id)
        self.assertEqual(user_document.id, " ")
        self.assertEqual(user_document.question, "No question")
        self.assertEqual(user_document.tz, "No TZ")
        self.assertEqual(user_document.deadline, "No deadline")
        self.assertEqual(user_document.contacts, "No contacts")
        self.assertEqual(user_document.category, CategoriesEnum.NEW)
        self.assertIsInstance(user_document.start_date, datetime)

    def test_bad_case_create_model(self):
        """
        Проверяет случай, когда user_id не является числом
        """
        user_id = "invalid_user_id"

        with self.assertRaises(ValueError) as context:
            UserDocument.create_model(user_id)

        self.assertEqual(str(context.exception),
                         "invalid literal for int() with base 10: 'invalid_user_id'")


if __name__ == '__main__':
    unittest.main()
