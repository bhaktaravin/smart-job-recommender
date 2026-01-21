from typing import Optional

from pydantic import BaseModel, HttpUrl


class JobCreate(BaseModel):
    title: str
    company: str
    location: Optional[str] = None
    description: Optional[str] = None
    url: Optional[HttpUrl] = None  # validates proper URLs
