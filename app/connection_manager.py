import asyncio
from operator import itemgetter
from typing import Dict, Set, Tuple

from broadcaster import Broadcast  # type: ignore
from fastapi import WebSocket
from starlette.websockets import WebSocketState

from app.configs import settings
from app.dtos.chat_response import MessageToRoomResponse


class ConnectionManager:
    """
    이 클래스는 WebSocket 연결 및 메시지 브로드캐스팅을 관리합니다.
    """

    broadcaster = Broadcast(settings.REDIS_URL)

    def __init__(self) -> None:
        """
        연결 및 사용자를 추적하는 딕셔너리로 인스턴스를 초기화합니다.
        """
        self.connections: Dict[str, Set[int]] = {}  # 각 방에 연결된 사용자를 추적합니다.
        self.user_connections: Dict[int, WebSocket] = {}  # 사용자 ID와 WebSocket 연결을 추적합니다.

    async def connect_broadcaster(self) -> None:
        await self.broadcaster.connect()

    async def disconnect_broadcaster(self) -> None:
        await self.broadcaster.disconnect()

    async def save_user_connection_record(self, ws_connection: WebSocket, user_id: int) -> None:
        """
        사용자의 WebSocket 연결 레코드를 저장합니다.
        """
        self.user_connections[user_id] = ws_connection
        await self._send_message_to_ws_connection(message="연결 성공", ws_connection=ws_connection)

    async def add_user_connection_to_room(self, room_id: str, user_id: int) -> Tuple[bool, str]:
        """
        사용자를 방에 추가합니다.
        """
        user_ws_connection = self.user_connections.get(user_id, None)

        if user_ws_connection is None:
            return False, "사용자를 찾을 수 없습니다"

        is_connection_active = await self._check_if_ws_connection_is_still_active(user_ws_connection)

        if not is_connection_active:
            self.user_connections.pop(user_id)
            return False, "비활성화된 연결입니다"

        if room_id not in self.connections.keys():
            self.connections[room_id] = {user_id}

            subscribe_n_listen_task = asyncio.create_task(self._subscribe_and_listen_to_channel(room_id=room_id))
            wait_for_subscribe_task = asyncio.create_task(asyncio.sleep(1))

            await asyncio.wait([subscribe_n_listen_task, wait_for_subscribe_task], return_when=asyncio.FIRST_COMPLETED)
        else:
            self.connections[room_id].add(user_id)

        return True, "연결 성공"

    async def _check_if_ws_connection_is_still_active(self, ws_connection: WebSocket, message: str = ".") -> bool:
        """
        WebSocket 연결이 여전히 활성 상태인지 확인합니다.
        """
        if not (
            ws_connection.application_state == WebSocketState.CONNECTED
            and ws_connection.client_state == WebSocketState.CONNECTED
        ):
            return False

        try:
            await ws_connection.send_text(message)
        except RuntimeError:
            return False

        return True

    async def _consume_events(self, message: MessageToRoomResponse) -> None:
        """
        채널에서 메시지를 수신합니다.
        """
        room_connections = self.connections.get(message.room_id, set())
        if len(room_connections) == 0:
            return
        users_ws_connections = itemgetter(*room_connections)(self.user_connections)

        if not isinstance(users_ws_connections, tuple):
            users_ws_connections = [users_ws_connections]

        for connection in users_ws_connections:
            is_sent, sent_message_response_info = await self._send_message_to_ws_connection(
                message=f"방 {message.room_id} --> {message.message}", ws_connection=connection
            )

    async def _subscribe_and_listen_to_channel(self, room_id: str) -> None:
        """
        채널을 구독하고 메시지를 수신합니다.
        """
        async with self.broadcaster.subscribe(room_id) as subscriber:
            async for event in subscriber:
                # print(event.message)
                message = MessageToRoomResponse.model_validate_json(event.message)
                await self._consume_events(message=message)

    async def send_message_to_room(self, room_id: str, message: str, user_nickname: str, user_id: int) -> None:
        """
        방에 있는 모든 사용자에게 메시지를 보냅니다.
        """
        room_connections = self.connections.get(room_id, set())
        if len(room_connections) == 0:
            return

        users_ws_connections = itemgetter(*room_connections)(self.user_connections)
        if not isinstance(users_ws_connections, tuple):
            users_ws_connections = [users_ws_connections]

        for connection in users_ws_connections:
            await self._send_message_to_ws_connection(message=f"{user_nickname}-->{message}", ws_connection=connection)

    async def _send_message_to_ws_connection(self, message: str, ws_connection: WebSocket) -> Tuple[bool, str]:
        """
        WebSocket 연결에 메시지를 보냅니다.
        """
        try:
            await ws_connection.send_text(message)
            return True, "메시지 전송됨"
        except RuntimeError:
            return False, "메시지 전송 실패, WebSocket이 연결 해제됨"

    def remove_user_connection(self, user_id: int) -> None:
        """
        사용자의 연결을 제거합니다.
        """
        self.user_connections.pop(user_id)
