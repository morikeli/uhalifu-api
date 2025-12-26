from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.schemas import LocationResponse
from app.services import LocationService


router = APIRouter()


async def get_location_service(db: AsyncSession = Depends(get_db)) -> LocationService:
    return LocationService(db=db)


@router.get("/locations", response_model=List[LocationResponse])
async def fetch_all_locations(
    offset: int = 0,
    limit: int = Query(100, le=5000),
    service: LocationService = Depends(get_location_service),
):
    return await service.get_locations(offset=offset, limit=limit)
