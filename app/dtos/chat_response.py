from pydantic import BaseModel


class RegisterToRoomResponse(BaseModel):
    user_id: int
    room_id: str


class MessageToRoomResponse(BaseModel):
    user_id: int
    message: str
    room_id: str
