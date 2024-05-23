from fastapi import APIRouter, Depends, WebSocket
from starlette.responses import FileResponse

from app.connection_manager import ConnectionManager
from app.dtos.chat_response import MessageToRoomBaseResponse
from app.services.chat_service import (
    service_register_user_to_room,
    service_websocket_endpoint,
)
from app.services.user_service import get_current_user

router = APIRouter(prefix="/api/v1/chat", tags=["chat"], redirect_slashes=False)

connection_manager = ConnectionManager()


@router.get("/")
async def get() -> FileResponse:
    return FileResponse("app/static/index.html")


@router.post("/register_to_room/")
async def register_user_to_room(body: MessageToRoomBaseResponse, current_user: int = Depends(get_current_user)) -> None:
    await service_register_user_to_room(body, current_user)


@router.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket, current_user: int = Depends(get_current_user)) -> None:
    await service_websocket_endpoint(current_user, websocket)


# 채팅방 나가는 로직 짤 예정
