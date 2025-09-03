

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.responses import ORJSONResponse

from schemas.tour import TourSchema
from services.ai_servise import AIService
from utils.utils import get_travel_days

tour_router = APIRouter(tags=["tour"])


def ai_service() -> AIService:
    return AIService()


@tour_router.post("/tour")
async def create_tour(
        data: TourSchema,
        service: AIService = Depends(ai_service)):
    days = get_travel_days(data.when, data.when_back)
    text_for_ai = (f'I want to go to {data.to} and I need you to show me the 5 best places and tell me the '
                   f'approximate cost for {days} days.')
    return_text = await service.ai_text_generator(text_for_ai)

    image = await service.handle_image(f'Create photo{data.to} ')
    return ORJSONResponse({
        'messages': return_text,
        'image_base64': image
    })
