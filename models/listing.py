from pydantic import BaseModel
from typing import List, Optional

class Listing(BaseModel):
    platform: str
    title: str
    description: str
    tags: List[str]
    suggested_price: Optional[float] = None