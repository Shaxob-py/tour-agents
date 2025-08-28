from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.responses import ORJSONResponse
from h11 import Response
from starlette import status
from core.config import settings
from schemas.ai_schema import ChatAiSchema
from schemas.base_schema import ResponseSchema
from services.otp_services import OtpService
from utils.utils import generate_code
import requests

ai_router = APIRouter()
API_URL = 'https://openrouter.ai/api/v1/chat/completions'


@ai_router.get('/ai-chat')
async def handle_message(message):
    user_text = message

    print(user_text)
    headers = {
        "Authorization": f"Bearer {settings.AI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": settings.AI_MODEL,
        "messages": [
            {"role": "system", "content": '''My job is to help you with almost anything you need, for example:
✅ Answering your questions, even complex ones.
✅ Your message should not up 4230.
✅ Helping you write or understand code (Python, JS, etc.).
✅ Finding and explaining free AI APIs you can use.
✅ Supporting you with projects like Telegram bots, web apps, or AI models.
✅ Helping you study English, create study plans, or learn new skills.
✅ Or simply being someone to chat with whenever you want and you have to speak an Uzbek language'''},
            {"role": "user", "content": user_text}
        ]
    }
    response = requests.post(API_URL, json=payload, headers=headers)
    print(response.json())
    if response.ok:
        answer = response.json()['choices'][0]['message']['content']
        return ResponseSchema[ChatAiSchema](
            message=answer,
            chat=user_text
        )
    else:
        return ResponseSchema[ChatAiSchema](
            message='Ai not found',
            chat=user_text
        )

# return ResponseSchema[ReadCategory](
#         message=f'Category {category.id} was created.',
#         data=category
#     )
