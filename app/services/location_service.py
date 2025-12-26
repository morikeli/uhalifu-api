from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from typing import Optional
from app.models import Location


class LocationService:
    def __init__(self, db):
        self.db = db

    async def get_locations(self, offset: int, limit: int = 10):
        """
        Get all locations from the db.
        """
        query = await self.db.execute(select(Location).offset(offset).limit(limit))
        return query.scalars().all()

    async def filter_by_location(
        self,
        country: Optional[str] = None,
        city: Optional[str] = None,
        province: Optional[str] = None,
        region: Optional[str] = None,
        year: Optional[int] = date.year,
        month: Optional[date.month] = None,
        day: Optional[date.day] = None,
        suicide_attack: Optional[bool] = None,
    ):
        """
        Filter by:
            - country
            - region
            - year
            - month
            - province
        """

        stmt = select(Location).where(
            Location.country == country,
            Location.year == year,
        )

        if city:
            stmt = stmt.where(Location.city == city)

        if province:
            stmt = stmt.where(Location.province == province)

        if region:
            stmt = stmt.where(Location.region == region)

        if month:
            stmt = stmt.where(Location.month == month)

        if day:
            stmt = stmt.where(Location.day == day)
        
        if suicide_attack:
            stmt = stmt.where(Location.suicide_bombing == suicide_attack)

        result = await self.db.execute(stmt)
        return result.scalars().all()
