from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
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


@router.get("/location", response_model=List[LocationResponse])
async def filter_location(
    offset: Optional[int] = Query(0, ge=0),
    limit: Optional[int]  = Query(100, ge=0, le=1000),
    country: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    province: Optional[str] = Query(None),
    year: Optional[int] = Query(None, gt=1970),
    month: Optional[int] = Query(None, le=1, ge=12),
    day: Optional[int] = Query(None, le=1, ge=31),
    suicide_attack: Optional[bool] = Query(False),
    service: LocationService = Depends(get_location_service),
):
    return await service.filter_by_location(
        offset=offset,
        limit=limit,
        country=country,
        city=city,
        region=region,
        year=year,
        month=month,
        day=day,
        province=province,
        suicide_attack=suicide_attack,
    )
