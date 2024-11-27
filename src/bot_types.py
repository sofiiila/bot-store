from typing import Optional

from pydantic import BaseModel


class InvoiceDataType(BaseModel):
    user_id: int
    question: Optional[str] = "No question"
    tz: Optional[str] = "No TZ"
    files: Optional[list] = "No files"
    deadline: Optional[str] = "No deadline"
    contacts: Optional[str] = "No contacts"
