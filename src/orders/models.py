from sqlalchemy import (
    Integer, String,
    Table, Column, ForeignKey
)

from src.auth.models import user
from src.database import metadata


request = Table(
    "request",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("status", String, nullable=False),
    Column("request_user_id", Integer, ForeignKey(user.c.id)),
)


response = Table(
    "response",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("response_user_id", Integer, ForeignKey(user.c.id)),
    Column("request_id", Integer, ForeignKey(request.c.id)),
    Column("message", String),
)
