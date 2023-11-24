from pydantic import BaseModel


class RequestCreate(BaseModel):
    id: int
    name: str
    status: str
    request_user_id: int


class ResponseCreate(BaseModel):
    id: int
    response_user_id: int
    request_id: int
    message: str
