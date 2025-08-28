import uvicorn
from fastapi import FastAPI
from uvicorn import lifespan

from routers import router

app = FastAPI(docs_url='/', root_path='/api', title="P30 FastAPI")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

app.include_router(router)
if __name__ == "__main__":
    uvicorn.run(app)


