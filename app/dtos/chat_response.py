from pydantic import BaseModel


class MessageToRoomBaseResponse(BaseModel):
    room_id: str
    user_id: int


class MessageToRoomResponse(MessageToRoomBaseResponse):
    message: str
