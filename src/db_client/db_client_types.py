"""
models
"""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class CategoriesEnum(str, Enum):
    """
    Categories
    """
    NEW = "new"
    QUEUE = "queue"
    INVALID = "invalid"
    IN_PROGRESS = "in_progress"


class UserDocument(BaseModel):
    """
    user data model
    """
    id: str = " "
    user_id: int
    question: str = "No question"
    tz: str = "No TZ"
    deadline: str = "No deadline"
    contacts: str = "No contacts"
    category: CategoriesEnum = CategoriesEnum.NEW
    start_date: datetime = datetime.now()

    @classmethod
    def create_model(cls, user_id):
        """
        create
        :param user_id:
        :return:
        """
        return UserDocument(user_id=int(user_id))

    def to_api(self):
        """
        method
        :return:
        """
        api_data = {}
        for key, value in self.dict().items():
            if isinstance(value, datetime):
                api_data[key] = value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            else:
                api_data[key] = value
        return api_data
