from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.responses import ORJSONResponse

# from routers.ai import handle_image
from schemas.tour import TourSchema
from services.ai_servise import AIService
from utils.security import get_current_user
from utils.utils import get_travel_days

tour_router = APIRouter(tags=["tour"])


def ai_service() -> AIService:
    return AIService()


@tour_router.post("/tour")
async def create_tour(
        data: TourSchema,
        service: AIService = Depends(ai_service),
        current_user = Depends(get_current_user),
        ):
    days = get_travel_days(data.when, data.when_back)
    text_for_ai = (f'I want to go to {data.to} and I need you to show me the 5 best places and tell me the '
                   f'approximate cost for {days} days.')
    return_text = await service.ai_text_generator(text_for_ai)
    image = await service.handle_image_unsplash(f'{data.to}')
    return ORJSONResponse({'messages': return_text,
                           'image': image})
