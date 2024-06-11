from pydantic import BaseModel
from uuid import UUID

class Portfolio(BaseModel):
    name: str
    id: UUID

