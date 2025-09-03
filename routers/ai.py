import base64
import io

import httpx
from fastapi import APIRouter
from starlette.responses import StreamingResponse

from core.config import settings
from schemas.ai_schema import ChatAiSchema
from schemas.base_schema import ResponseSchema

ai_router = APIRouter()


@ai_router.post('/ai-chat')
async def handle_message(message: ChatAiSchema):
    user_text = message.message   # agar ChatAiSchema da "message" field bo‘lsa
    headers = {
        "Authorization": f"Bearer {settings.GEMINI_AI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": settings.GEMINI_AI_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful AI tour agent."},
            {"role": "user", "content": user_text}
        ]

    }
    async with httpx.AsyncClient() as client:
        response = httpx.post(settings.AI_URL, json=payload, headers=headers)

    if response.status_code == 200:
        answer = response.json()['choices'][0]['message']['content']
        return ResponseSchema[ChatAiSchema](
            message=answer,
            chat=user_text
        )
    else:
        return ResponseSchema[ChatAiSchema](
            message='Ai not found',
            chat=user_text)







@ai_router.post("/ai-image")
async def handle_image(message: str):
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
    return StreamingResponse(buf, media_type="image/png", headers=headers)

    # TODO service ga otkazish

    # TODO chatgpt dan 2hil tilda (uz, en) malumot qaytarish va db ga saqlash

    # TODO chatgpt dan qaytgan textni image ai ga yuborib qaytgan imagelarni db ga saqlash
