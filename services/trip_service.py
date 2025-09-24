from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import Optional
from datetime import date

from database.trips import Trip
from schemas.base_schema import ReadTripSchema


class TripService:
    @staticmethod
    async def list_trips(
            session: AsyncSession,
            search: Optional[str] = None,
            destination: Optional[str] = None,
            start_date: Optional[date] = None,
            end_date: Optional[date] = None,
            skip: int = 0,
            limit: int = 10,
    ):
        query = select(Trip).options(
            selectinload(Trip.created_by),
            selectinload(Trip.images)
        )

        if search:
            query = query.filter(
                (Trip.destination.ilike(f"%{search}%"))
                | (Trip.description.ilike(f"%{search}%"))
            )

        if destination:
            query = query.filter(Trip.destination.ilike(f"%{destination}%"))
        if start_date:
            query = query.filter(Trip.start_date >= start_date)
        if end_date:
            query = query.filter(Trip.end_date <= end_date)

        count_query = select(func.count(Trip.id)).select_from(Trip)

        if search:
            count_query = count_query.filter(
                (Trip.destination.ilike(f"%{search}%"))
                | (Trip.description.ilike(f"%{search}%"))
            )
        if destination:
            count_query = count_query.filter(Trip.destination.ilike(f"%{destination}%"))
        if start_date:
            count_query = count_query.filter(Trip.start_date >= start_date)
        if end_date:
            count_query = count_query.filter(Trip.end_date <= end_date)

        total_count = await session.scalar(count_query)

        query = query.offset(skip).limit(limit)
        result = await session.execute(query)
        trips = result.scalars().all()
        return {
            "count": total_count or 0,
            "skip": skip,
            "limit": limit,
            "items": [ReadTripSchema.model_validate(trip) for trip in trips],
        }
