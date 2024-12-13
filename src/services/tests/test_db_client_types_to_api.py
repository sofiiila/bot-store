import unittest
from datetime import datetime
from src.services.db_client_types import UserDocument, CategoriesEnum


class TestUserDocument(unittest.TestCase):

    def test_good_case_to_api(self):
        """
        Проверяет успешное преобразование данных в формат API
        """
        user_id = 1
        user_document = UserDocument(
            id="12345",
            user_id=user_id,
            question="What is the meaning of life?",
            tz="UTC",
            files="file1.txt",
            deadline="2023-12-31",
            contacts="contact@example.com",
            category=CategoriesEnum.IN_PROGRESS,
            start_date=datetime(2023, 10, 1, 12, 0, 0)
        )

        api_data = user_document.to_api()

        expected_api_data = {
            "id": "12345",
            "user_id": 1,
            "question": "What is the meaning of life?",
            "tz": "UTC",
            "files": "file1.txt",
            "deadline": "2023-12-31",
            "contacts": "contact@example.com",
            "category": CategoriesEnum.IN_PROGRESS,
            "start_date": "2023-10-01T12:00:00.000000Z"
        }

        self.assertEqual(api_data, expected_api_data)
        
# test_bad_case_to_api.py не будет потому что Pydantic не дает создать модель с некорректными данными


if __name__ == '__main__':
    unittest.main()
