from enum import Enum
from typing import Optional

from pydantic import BaseModel
from pymongo.results import InsertOneResult


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

    @classmethod
    def create_model(cls, user_id):
        return UserDocument(user_id=int(user_id))