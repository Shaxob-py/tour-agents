from uuid import UUID
from datetime import datetime
from http.client import HTTPException

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from const import TOUR_PROMPT
from database import Trip
from database.base_model import get_session
from database.trips import TripLike, TripImage
from schemas.base_schema import TripSchema, ResponseSchema, ReadTripSchema, APIResponse
from services.ai_servise import AIService, ai_service
from utils.security import get_current_user
from utils.utils import get_travel_days

trip_agents = APIRouter(tags=["tour"])


@trip_agents.post("/trip",response_model=APIResponse)
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
        start_date=start_date,
        end_date=end_date,
        user_id=current_user.id,
        is_ai_suggestion=True
    )

    await TripImage.create(
        trip_id=trip.id,
        url=image,
    )
    return ORJSONResponse({
        'messages': return_text,
        'image': image})


@trip_agents.post("/{trip_id}/like")

async def like_dislike_trip(
        trip_id: UUID,
        is_like: bool,
        session: AsyncSession = Depends(get_session),
        user=Depends(get_current_user),
):

    trip =  Trip.get(trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    result = await session.execute(
        select(TripLike).where(
            TripLike.trip_id == trip_id,
            TripLike.user_id == user.id
        )
    )
    trip_like = result.scalar_one_or_none()

    if trip_like:
        trip_like.is_like = is_like
    else:
        trip_like = TripLike(
            trip_id=trip_id,
            user_id=user.id,
            is_like=is_like
        )
        session.add(trip_like)

    await session.commit()
    return {"message": "Success", "trip_id": str(trip_id), "is_like": is_like}


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


@trip_agents.get("/trip",response_model=ResponseSchema)
async def get_tour():

    tours = await Trip.get_all()
    return ResponseSchema[list[ReadTripSchema]](
        message='All Tours',
        data=tours,
    )


@trip_agents.get("/trip{id}",response_model=ReadTripSchema)
async def get_tour_id(id: UUID):
    trip = await Trip.get(id)
    if trip is None:
        return ORJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={'message': 'trip not found', 'data': None}
        )
    await Trip.update_view_count(id)

    return ResponseSchema[ReadTripSchema](
        message='Trip detail',
        data=trip
    )
