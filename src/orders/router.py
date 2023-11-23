from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import current_user
from src.auth.models import User
from src.database import get_async_session

from src.orders.models import request
from src.orders.schemas import RequestCreate

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.get("/")
async def get_all_requests(session: AsyncSession = Depends(get_async_session)):
    query = select(request).where(request.c.status == "working")
    result = await session.execute(query)
    return result.mappings().all()


@router.get("/{request_id}/")
async def get_request_by_id(request_id: int, session: AsyncSession = Depends(get_async_session)):
    print(request_id)
    query = select(request).where(request.c.id == request_id)
    result = await session.execute(query)
    return result.mappings().all()


@router.post("/add/")
async def add_request(
        new_order: RequestCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    stmt = insert(request).values(**new_order.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
