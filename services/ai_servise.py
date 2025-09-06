import os
from datetime import datetime

import aiofiles
import httpx
from starlette import status

from core.config import settings

UNSPLASH_ACCESS_KEY = settings.UNSPLASH_ACCESS_KEY


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
            "max_tokens": 100,

        }
        async with httpx.AsyncClient() as client:
            response = await client.post(settings.AI_URL, json=payload, headers=headers)

        if response.status_code == status.HTTP_200_OK:
            answer = response.json()['choices'][0]['message']['content']
            return answer
        else:
            return text

    # async def handle_image(self, message: str):
    #     headers = {
    #         "Authorization": f"Bearer {settings.GEMINI_AI_API_KEY}",
    #         "Content-Type": "application/json"
    #     }
    #     payload = {
    #         "prompt": message,
    #         "model": settings.GEMINI_AI_MODEL,
    #         "size": "512x512",
    #         "n": 1
    #     }
    #
    #     async with httpx.AsyncClient() as client:
    #         response = await client.post(settings.AI_URL, json=payload, headers=headers)
    #
    #         try:
    #             data = response.json()
    #             image_url = data.get("choices", [{}])[0].get('images')[0].get('image_url').get('url')
    #             return image_url
    #         except:
    #             return None

    async def handle_image_unsplash(self, query: str) -> str | None:
        url = "https://api.unsplash.com/search/photos"
        params = {"query": query, "per_page": 1}  # faqat 1 ta rasm
        headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}

        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            resp = await client.get(url, params=params, headers=headers)
            if resp.status_code != status.HTTP_200_OK:
                print("Unsplash API error:", resp.status_code, resp.text)
                return None

            data = resp.json()
            results = data.get("results")
            if not results:
                print("No results for query:", query)
                return None

            image_url = results[0]["urls"]["regular"]

            img_resp = await client.get(image_url)
            if img_resp.status_code != status.HTTP_200_OK:
                print("Image download failed:", img_resp.status_code)
                return None

            save_dir = os.path.join("media", "tours")
            os.makedirs(save_dir, exist_ok=True)
            filename = f"tour_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            file_path = os.path.join(save_dir, filename)

            async with aiofiles.open(file_path, "wb") as f:
                await f.write(img_resp.content)

            return os.path.join("/media/tours", filename)


def ai_service() -> AIService:
    return AIService()
