from pydantic import BaseModel

class CircleCreate(BaseModel):
    name: str
    category: str
    description: str | None = None