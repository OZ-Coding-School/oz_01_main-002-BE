from fastapi import APIRouter, WebSocket
from starlette.responses import FileResponse

from app.connection_manager import ConnectionManager
from app.dtos.chat_response import MessageToRoomBaseResponse
from app.services.chat_service import (
    service_register_user_to_room,
    service_websocket_endpoint,
)

router = APIRouter(prefix="/api/v1/chat", tags=["chat"], redirect_slashes=False)

connection_manager = ConnectionManager()


@router.on_event("startup")
async def startup() -> None:
    print("Connecting to redis")
    await connection_manager.connect_redis()
    print("Connected to redis")


@router.on_event("shutdown")
async def shutdown() -> None:
    print("Disconnecting from redis")
    await connection_manager.disconnect_redis()
    print("Disconnected from redis")


@router.get("/")
async def get() -> FileResponse:
    return FileResponse("app/static/index.html")


@router.post("/register_to_room/")
async def register_user_to_room(body: MessageToRoomBaseResponse) -> None:
    await service_register_user_to_room(body)


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(user_id: int, websocket: WebSocket) -> None:
    await service_websocket_endpoint(user_id, websocket)


# 채팅방 나가는 로직 짤 예정
