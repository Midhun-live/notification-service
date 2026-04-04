from fastapi import FastAPI
from app.core.database import engine
from app.api.user_preferences import router as user_preferences_router
from app.api.notifications import router as notifications_router

app = FastAPI()

app.include_router(user_preferences_router)
app.include_router(notifications_router)

@app.get("/")
def root():
    return {"status": "Running"}