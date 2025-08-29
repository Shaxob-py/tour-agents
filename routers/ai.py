from fastapi import APIRouter
from core.config import settings
from schemas.ai_schema import ChatAiSchema
from schemas.base_schema import ResponseSchema
import httpx

ai_router = APIRouter()
API_URL = 'https://openrouter.ai/api/v1/chat/completions'


@ai_router.get('/ai-chat')
async def handle_message(message:ChatAiSchema):
    user_text = message
    headers = {
        "Authorization": f"Bearer {settings.GEMINI_AI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": settings.AI_MODEL,
        "messages": [
            {"role": "system", "content": '''My job is to help you with almost anything you need, for example:
            ✅ Answering your questions, even complex ones.
            sen tour agets xodimisan va sen odamlarga togri joy tanlab beriishing kerak'''},
            {"role": "user", "content": user_text}
        ]
    }
    response = httpx.post(API_URL, json=payload, headers=headers)
    print(response.json())
    if response.status_code == 200:
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


