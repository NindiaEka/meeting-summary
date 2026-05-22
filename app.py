from fastapi import FastAPI

from app.routers.summarize import router


app = FastAPI()


app.include_router(router)


@app.get("/")
def root():

    return {
        "message": "AI MoM Notetaker API is running"
    }