import traceback

from fastapi import WebSocket, WebSocketDisconnect, WebSocketException
from fastapi.exceptions import HTTPException

from app.connection_manager import ConnectionManager
from app.dtos.chat_response import MessageToRoomBaseResponse
from app.models.chat import MessageToRoomModel
from app.models.users import User

# 현재 웹소켓 연결 수의 변수
number_of_socket_connections = 0

connection_manager = ConnectionManager()


async def service_register_user_to_room(body: MessageToRoomBaseResponse, current_user: int) -> dict[str, str]:
    """
    이 함수는 사용자를 채팅방에 등록함.
    """
    # 사용자를 채팅방에 추가하고 결과 및 메시지를 반환.
    is_added, message = await connection_manager.add_user_connection_to_room(user_id=current_user, room_id=body.room_id)

    if not is_added:
        raise HTTPException(detail={"message": message}, status_code=400)

    # 채팅 기록을 가져와서 사용자에게 전송함.
    chat_history = await MessageToRoomModel.get_chat_history_for_room(room_id=body.room_id)
    for chat_message in chat_history:
        sender_user = await User.get_by_user_id(chat_message.user_id)
        if sender_user:
            message_to_send = f"{sender_user.nickname}: {chat_message.message}"
            await connection_manager.send_message_to_user(message=message_to_send, user_id=current_user)

    return {"message": message}


async def service_websocket_endpoint(current_user: int, websocket: WebSocket) -> None:
    """
    웹소켓 연결을 처리하는 함수.
    """

    # 클라이언트의 웹소켓 연결
    await websocket.accept()
    global number_of_socket_connections

    # 사용자 아이디로부터 사용자 정보를 가져옴.
    user = await User.get_by_user_id(current_user)
    if not user:
        await websocket.close()
        return

    # 사용자를 연결 스택에 추가.
    await connection_manager.save_user_connection_record(user_id=current_user, ws_connection=websocket)

    try:
        # 웹소켓 연결 수를 증가.
        number_of_socket_connections += 1

        while True:
            # 클라이언트로부터 메시지를 받음.
            data = await websocket.receive_json()

            # 받은 메시지를 채팅방의 모든 사용자에게 전송함.
            room_id = data["room_id"]
            message = data["message"]

            await MessageToRoomModel.create_by_message(room_id=room_id, message=message, user_id=current_user)

            await connection_manager.send_message_to_room(
                message=message, room_id=room_id, user_nickname=user.nickname, ws_connection=websocket
            )
    except WebSocketDisconnect:
        # 웹소켓 연결이 끊긴 경우, 사용자를 연결 스택에서 제거.
        connection_manager.remove_user_connection(user_id=current_user)
    except WebSocketException as e:
        traceback.print_exc()
