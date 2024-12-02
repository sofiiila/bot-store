from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class CategoriesEnum(str, Enum):
    new = "new"
    queue = "queue"
    invalid = "invalid"
    in_progress = "in_progress"


class UserDocument(BaseModel):
    id: str = " "
    user_id: int
    question: str = "No question"
    tz: str = "No TZ"
    files: str = "No files"
    deadline: str = "No deadline"
    contacts: str = "No contacts"
    category: CategoriesEnum = CategoriesEnum.new
    start_date: datetime = datetime.now()

    @classmethod
    def create_model(cls, user_id):
        return UserDocument(user_id=int(user_id))

    def to_api(self):
        api_data = {}
        for key, value in self.dict().items():
            if isinstance(value, datetime):
                api_data[key] = value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            else:
                api_data[key] = value
        return api_data
