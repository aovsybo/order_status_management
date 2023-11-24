from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import current_user
from src.auth.models import User
from src.database import get_async_session

from src.orders.models import request, response
from src.orders.schemas import RequestCreate, ResponseCreate

request_router = APIRouter(
    prefix="/requests",
    tags=["requests"],
)

response_router = APIRouter(
    prefix="/responses",
    tags=["responses"],
)


@request_router.get("/")
async def get_all_requests(session: AsyncSession = Depends(get_async_session)):
    query = select(request)
    result = await session.execute(query)
    return result.mappings().all()


@request_router.get("/{request_id}/")
async def get_request_by_id(request_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(request).where(request.c.id == request_id)
    result = await session.execute(query)
    return result.mappings().all()


@request_router.post("/add/")
async def add_request(
        new_request: RequestCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    stmt = insert(request).values(**new_request.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@response_router.get("/income/")
async def get_income_requests(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    query = (select(response)
             .join(request, response.c.request_id == request.c.id)
             .where(request.c.request_user_id == user.id))
    result = await session.execute(query)
    return result.mappings().all()


@response_router.post("/add/")
async def add_response(
        new_response: ResponseCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    request_query = select(request).where(request.c.id == new_response.request_id)
    result = await session.execute(request_query)
    if result.mappings().first()["request_user_id"] != user.id:
        stmt = insert(response).values(**new_response.dict())
        await session.execute(stmt)
        await session.commit()
        return {"status": "success"}
    else:
        return {"status": "failed", "message": "you can not response to yourself"}
