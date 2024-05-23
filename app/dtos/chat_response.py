from pydantic import BaseModel


class MessageToRoomBaseResponse(BaseModel):
    room_id: str


class MessageToRoomResponse(MessageToRoomBaseResponse):
    message: str
