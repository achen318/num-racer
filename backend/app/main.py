from app.api.routes import rooms
from app.ws.manager import WebSocketManager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rooms.router)


ws_manager = WebSocketManager()


@app.websocket("/ws/{room_id}/{player}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, player: str):
    await ws_manager.connect(room_id, websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await ws_manager.broadcast(data)
    except WebSocketDisconnect:
        ws_manager.disconnect(room_id, websocket)
