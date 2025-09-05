from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.responses import ORJSONResponse

# from routers.ai import handle_image
from schemas.tour import TourSchema
from services.ai_servise import AIService, ai_service
from utils.security import get_current_user
from utils.utils import get_travel_days

tour_router = APIRouter(tags=["tour"])


@tour_router.post("/tour")
async def create_tour(
        data: TourSchema,
        service: AIService = Depends(ai_service),
        current_user=Depends(get_current_user),
):
    days = get_travel_days(data.when, data.when_back)
    text_for_ai = (f'I want to go to {data.to} and I need you to show me the 5 best places and tell me the '
                   f'approximate cost for {days} days.')
    # TODO const.py alohida ochilib osha yerga yozish kk
    return_text = await service.ai_text_generator(text_for_ai)
    image = await service.handle_image_unsplash(f'{data.to}')
    return ORJSONResponse({'messages': return_text,
                           'image': image})

    # TODO image larni saqlash kk
    # TODO ai dan qaytgan text larni ham saqlash kk
    # TODO /trip history qaytaradigan bolsin
    # TODO like & dislike uchun api
