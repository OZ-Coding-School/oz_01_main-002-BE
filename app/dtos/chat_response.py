from pydantic import BaseModel


class MessageToRoomBaseResponse(BaseModel):
    user_id: int
    room_id: str


class MessageToRoomResponse(MessageToRoomBaseResponse):
    message: str
