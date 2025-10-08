from datetime import datetime, date
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Query, HTTPException
from fastapi.params import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.sync import update
from starlette import status
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from const import TOUR_PROMPT
from database import Trip, User
from database.base_model import get_session, db
from database.trips import TripLike, TripImage
from schemas.base_schema import TripSchema, ResponseSchema, ReadTripSchema, TripLikeRequest, ListResponseSchema
from services.ai_servise import AIService, ai_service
from services.trip_service import TripService
from utils.security import get_current_user
from utils.utils import get_travel_days
from sqlalchemy import String, Date, Boolean, ForeignKey, Integer, update, delete
trip_agents = APIRouter(tags=["Trip"])


@trip_agents.post("/trips")
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
        user_id=current_user.id,  # noqa
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


@trip_agents.get("/trips", response_model=ListResponseSchema[ReadTripSchema])
async def list_trips(
        session: AsyncSession = Depends(get_session),
        search: Optional[str] = Query(None, description="Qidiruv (destination/description)"),
        destination: Optional[str] = Query(None, description="Manzil filter"),
        start_date: Optional[date] = Query(None, description="Boshlanish sanasi"),
        end_date: Optional[date] = Query(None, description="Tugash sanasi"),
        skip: int = Query(0, ge=0, description="Qaysidan boshlab olish"),
        limit: int = Query(10, ge=1, le=100, description="Nechta olish"),
):
    try:
        trip_list_paginated = await TripService.list_trips(
            session=session,
            search=search,
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            skip=skip,
            limit=limit,
        )
        return {
            "message": "Trip list",
            **trip_list_paginated
        }
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@trip_agents.post("/trips/like")
async def like_trip(data: TripLikeRequest, current_user: User = Depends(get_current_user)):
    await TripLike.update_like(data.trip_id, current_user.id, data.is_like)


@trip_agents.get("/trips/{id}", response_model=ResponseSchema[ReadTripSchema])
async def get_tour_id(id: UUID):



    trip = await Trip.get(id)

    if trip is None:
        return ORJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={'message': 'trip not found', 'data': None}
        )
    # trip.view_count += 1
    # await Trip.update_view_count(id)

    return ResponseSchema[ReadTripSchema](
        message='Trip detail',
        data=trip)
