from datetime import datetime, date
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Query
from fastapi.params import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from const import TOUR_PROMPT
from database import Trip
from database.base_model import get_session
from database.trips import TripLike, TripImage
from schemas.base_schema import TripSchema, ResponseSchema, ReadTripSchema, APIResponse, TripLikeRequest
from services.ai_servise import AIService, ai_service
from utils.security import get_current_user
from utils.utils import get_travel_days
from sqlalchemy.orm import selectinload

trip_agents = APIRouter(tags=["tour"])


@trip_agents.post("/trips", response_model=APIResponse)
async def create_tour(
        data: TripSchema,
        service: AIService = Depends(ai_service),
        current_user=Depends(get_current_user),
):
    days = get_travel_days(data.when, data.when_back)
    text_for_ai = TOUR_PROMPT.format(destination=data.to, days=days)
    return_text = await service.ai_text_generator(text_for_ai)
    image = await service.handle_image_unsplash(f'{data.to}')
    start_date = datetime.strptime(data.when, "%d.%m.%Y").date()
    end_date = datetime.strptime(data.when_back, "%d.%m.%Y").date()
    trip = await Trip.create(
        away_from=data.where,
        description=return_text,
        destination=data.to,
        days=days,
        start_date=start_date,
        end_date=end_date,
        user_id=current_user.id, # noqa
        is_ai_suggestion=True,
        likes_count=0,
        dislikes_count=0

    )

    await TripImage.create(
        trip_id=trip.id,
        url=image,
    )
    return ORJSONResponse({
        'messages': return_text,
        'image': image})

    # return {"message": "Success", "trip_id": str(trip_id), "is_like": is_like}


@trip_agents.get("/{trip_id}/like_statistics")
async def like_statistics(
        trip_id: UUID,
        session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(TripLike.is_like, func.count(TripLike.id))
        .where(TripLike.trip_id == trip_id)
        .group_by(TripLike.is_like)
    )
    stats = {True: 0, False: 0}
    for is_like, count in result.all():
        stats[is_like] = count

    return {
        "trip_id": str(trip_id),
        "likes": stats[True],
        "dislikes": stats[False],
    }


@trip_agents.post("/trips/like")
async def like(data: TripLikeRequest, current_user=Depends(get_current_user)):
    await TripLike.create_or_update(trip_id, current_user.id, is_like) # noqa
    await Trip.like_update(data.trip_id, data.is_like)
    return {"status": "ok"}




@trip_agents.get("/trips", response_model=APIResponse)
async def list_trips(
    session: AsyncSession = Depends(get_session),
    search: Optional[str] = Query(None),
    destination: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    query = (
        select(Trip)
        .options(
            selectinload(Trip.created_by),
            selectinload(Trip.images)
        )
    )

    if search:
        query = query.filter(
            (Trip.destination.ilike(f"%{search}%")) |
            (Trip.description.ilike(f"%{search}%"))
        )
    if destination:
        query = query.filter(Trip.destination.ilike(f"%{destination}%"))
    if start_date:
        query = query.filter(Trip.start_date >= start_date)
    if end_date:
        query = query.filter(Trip.end_date <= end_date)

    total_count = await session.scalar(
        select(func.count()).select_from(query.subquery())
    )

    query = query.offset(skip).limit(limit)
    result = await session.execute(query)
    trips = result.scalars().unique().all()

    return APIResponse(
        message="Trips retrieved successfully",
        data={
            "count": total_count,
            "items": [ReadTripSchema.model_validate(trip, from_attributes=True) for trip in trips]  # 👈
        }
    )


@trip_agents.get("/trips/{id}", response_model=ResponseSchema[ReadTripSchema])
async def get_tour_id(id: UUID):
    trip = await Trip.get(id)
    if trip is None:
        return ORJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={'message': 'trip not found', 'data': None}
        )
    await Trip.update_view_count(id) # noqa

    return ResponseSchema[ReadTripSchema](
        message='Trip detail',
        data=trip)


