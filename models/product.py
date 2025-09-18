from pydantic import BaseModel
from typing import Optional, List

class Product(BaseModel):
    title: str
    description: str
    price: Optional[float] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = []