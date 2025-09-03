import base64
import io

import httpx
from redis import Redis

from core.config import settings
from utils.utils import verification_send_telegram


class AIService:

    async def ai_text_generator(self, text):
        headers = {
            "Authorization": f"Bearer {settings.DEEPSEEK_AI_API_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": settings.DEEPSEEK_AI_MODEL,
            "messages": [
                {"role": "system",
                 "content": "You are a helpful AI tour agent and you should speak in Uzbek language."},
                {"role": "user", "content": text}
            ],
            "max_tokens": 300,

        }
        async with httpx.AsyncClient() as client:
            response = await client.post(settings.AI_URL, json=payload, headers=headers)

        if response.status_code == 200:
            answer = response.json()['choices'][0]['message']['content']
            return answer
        else:
            return text


    async def handle_image(self, message: str):
        headers = {
            "Authorization": f"Bearer {settings.GEMINI_AI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "prompt": message,
            "model": settings.GEMINI_AI_MODEL,
            "size": "512x512",
            "n": 1
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(settings.AI_URL, json=payload, headers=headers)

            try:
                data = response.json()
                image_url = data.get("choices", [{}])[0].get('images')[0].get('image_url').get('url')
                return image_url
            except:
                return None
