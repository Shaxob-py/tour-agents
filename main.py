import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

from admin import admin          # admin obyektini import qilamiz
from database.base_model import db
from routers import router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await db.create_all()
    admin.mount_to(app)          # shu yerda app ga mount qilamiz
    print('project ishga tushdi')
    yield
    print('project toxtadi')



app = FastAPI(
    docs_url='/',
    title="Tour Agency API",
    description="JWT Authentication bilan himoyalangan API",
    lifespan=lifespan,
)
MEDIA_DIR = os.path.join(os.getcwd(), "media")

if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR)

app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://10.40.1.161:3000",
    "http://10.40.1.161:8000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key="supersecretkey")
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT token kiriting (login qilib oling)"
        }
    }

    for path_data in openapi_schema["paths"].values():
        for operation in path_data.values():
            if isinstance(operation, dict) and "tags" in operation:
                if operation.get("tags") and "Public" not in operation["tags"]:
                    operation["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    msg = exc.args[0][0]['msg']
    return JSONResponse(
        {'message': msg},
        status.HTTP_400_BAD_REQUEST,
    )


app.include_router(router, prefix="/api/v1")
