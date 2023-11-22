from pydantic import BaseModel


class RequestCreate(BaseModel):
    id: int
    name: str
    status: str
    request_user_id: int
