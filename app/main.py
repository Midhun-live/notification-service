from fastapi import FastAPI
from app.core.database import engine
from app.api.user_preferences import router as user_preferences_router

app = FastAPI()

app.include_router(user_preferences_router)

@app.get("/")
def root():
    return {"status": "Running"}