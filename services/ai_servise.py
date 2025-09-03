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
                {"role": "system", "content": "You are a helpful AI tour agent and you should speak in Uzbek language."},
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
    # async def ai_text_generator(self, text: str) -> str:
    #     headers = {
    #         "Authorization": f"Bearer {settings.DEEPSEEK_AI_API_TOKEN}",
    #         "Content-Type": "application/json"
    #     }
    #
    #     payload = {
    #         "model": settings.DEEPSEEK_AI_MODEL,
    #         "messages": [
    #             {"role": "system", "content": "You are a helpful AI tour agent."},
    #             {"role": "user", "content": text}
    #         ],
    #         "max_tokens": 100,
    #     }
    #
    #     try:
    #         async with httpx.AsyncClient(timeout=30.0) as client:
    #             response = await client.post(settings.AI_URL, json=payload, headers=headers)
    #
    #         if response.status_code == 200:
    #             data = response.json()
    #             answer = data['choices'][0]['message']['content']
    #             return answer
    #         else:
    #             # Original text o'rniga error message
    #             return f"❌ AI service unavailable (Status: {response.status_code})"
    #
    #     except Exception as e:
    #         # Original text o'rniga error message
    #         return f"❌ AI service error: {str(e)}"

    async def handle_image(self,message: str):
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

        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.post(settings.AI_URL, json=payload, headers=headers)

        if response.status_code != 200:
            return {"error": response.text}

        try:
            data = response.json()
        except Exception:
            return {"error": "JSON decode xato", "raw": response.text}

        image_bytes = None

        if "choices" in data and len(data["choices"]) > 0:
            choice = data["choices"][0]

            if "images" in choice and len(choice["images"]) > 0:
                image_data = choice["images"][0]

                if "image_url" in image_data and "url" in image_data["image_url"]:
                    url = image_data["image_url"]["url"]

                    if url.startswith("data:image/"):
                        base64_start = url.find("base64,")
                        if base64_start != -1:
                            image_base64 = url[base64_start + 7:]  # Skip "base64,"
                            try:
                                image_bytes = base64.b64decode(image_base64)
                            except Exception as e:
                                return {"error": f"Base64 decode xato: {str(e)}", "raw": data}

                    else:
                        async with httpx.AsyncClient() as client:
                            img_resp = await client.get(url)
                        if img_resp.status_code == 200:
                            image_bytes = img_resp.content
                        else:
                            return {"error": f"Rasm URL'dan yuklab olinmadi: {img_resp.status_code}", "raw": data}

        if not image_bytes:
            if "data" in data and len(data["data"]) > 0 and "b64_json" in data["data"][0]:
                image_base64 = data["data"][0]["b64_json"]
                try:
                    image_bytes = base64.b64decode(image_base64)
                except Exception as e:
                    return {"error": f"Base64 decode xato: {str(e)}", "raw": data}


            elif "data" in data and len(data["data"]) > 0 and "url" in data["data"][0]:
                image_url = data["data"][0]["url"]
                async with httpx.AsyncClient() as client:
                    img_resp = await client.get(image_url)
                if img_resp.status_code == 200:
                    image_bytes = img_resp.content

        if not image_bytes:
            return {"error": "API'dan rasm topilmadi", "raw": data}

        buf = io.BytesIO(image_bytes)
        buf.seek(0)

        headers = {
            "Content-Disposition": "attachment; filename=generated.png"
        }
        return buf
