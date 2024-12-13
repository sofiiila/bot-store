import unittest

from src.services.db_client_types import UserDocument


class TestUserDocument(unittest.TestCase):
    def test_good_case_create_model(self):
        """Тест создания модели с валидным user_id."""
        pass

    def test_bad_case_create_model(self):
        """Тест создания модели с невалидным user_id."""
        invalid_user_id = "not_a_number"
        
        with self.assertRaises(ValueError):
            UserDocument.create_model(invalid_user_id)


if __name__ == '__main__':
    unittest.main()
