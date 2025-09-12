import uuid
from datetime import datetime
from http.client import HTTPException

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from const import TOUR_PROMPT
from database import Trip
from database.base_model import get_session
from database.trips import TripLike, TripImage
# from routers.ai import handle_image
from schemas.base_schema import TourSchema, ResponseSchema, ReadTourSchema
from services.ai_servise import AIService, ai_service
from utils.security import get_current_user
from utils.utils import get_travel_days

tour_router = APIRouter(tags=["tour"])

@tour_router.post("/trip")
async def create_tour(
        data: TourSchema,
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


@tour_router.post("/{trip_id}/like")
async def like_dislike_trip(
        trip_id: uuid.UUID,
        is_like: bool,
        session: AsyncSession = Depends(get_session),
        user=Depends(get_current_user),
):
    result = await session.execute(select(Trip).where(Trip.id == trip_id))
    trip = result.scalar_one_or_none()
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


@tour_router.get("/{trip_id}/like_statistics")
async def like_statistics(
        trip_id: uuid.UUID,
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


@tour_router.get("/history")
async def get_trip_history(
        session: AsyncSession = Depends(get_session),
        user=Depends(get_current_user),
):
    result = await session.execute(
        select(Trip)
        .where(Trip.user_id == user.id)
        .order_by(Trip.created_at.desc())
    )
    trips = result.scalars().all()

    if not trips:
        raise HTTPException(status_code=404, detail="No trips found in history")

    return [
        {
            "id": str(trip.id),
            "name": trip.name,
            "description": trip.description,
            "country": trip.country,
            "city": trip.city,
            "start_date": trip.start_date,
            "end_date": trip.end_date,
            "price": trip.price,
            "likes": trip.likes_count,
            "dislikes": trip.dislikes_count,
            "created_at": trip.created_at,
        }
        for trip in trips
    ]

# TODO api/v1/trips (id,away_from,destination,image,days,view_count,likes_count,dislikes_count)
# TODO api/v1/favorite (men like bosgan triplardagi ..dan ..gacha bolganlarini inobat olib chiqarish)

# uz -> kr
# kz -> kr
# kgz -> kr


@tour_router.get("/tours")
async def get_tour():
    tours = await Trip.get_all()
    return ResponseSchema[list[ReadTourSchema]](
        message='All Tours',
        data=tours,
    )
