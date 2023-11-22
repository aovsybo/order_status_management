from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session

from src.orders.models import request
from src.orders.schemas import RequestCreate

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.get("/")
async def get_requests(session: AsyncSession = Depends(get_async_session)):
    query = select(request).where(request.c.status == "working")
    result = await session.execute(query)
    row = result.mappings().all()
    return row


@router.post("/")
async def add_request(new_order: RequestCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(request).values(**new_order.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
