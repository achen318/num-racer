from fastapi import FastAPI

from api.routers import rooms, users

app = FastAPI()

app.include_router(rooms.router)
app.include_router(users.router)
