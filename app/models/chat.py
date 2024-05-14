from __future__ import annotations

from tortoise import fields
from tortoise.models import Model

from app.models.common import Common
from app.models.users import User


class RegisterToRoomModel(Common, Model):
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="reister_to_rooms", on_delete=fields.CASCADE
    )
    user_id: int
    room_id = fields.CharField(max_length=255)

    class Meta:
        table = "chatrooms"


class MessageToRoomModel(Common, Model):
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="message_to_rooms", on_delete=fields.CASCADE
    )
    user_id: int
    message = fields.TextField()
    room_id = fields.CharField(max_length=255)

    class Meta:
        table = "messages"

    @classmethod
    async def create_by_message(cls, user_id: int, room_id: str, message: str) -> MessageToRoomModel:
        return await cls.create(
            user_id=user_id,
            room_id=room_id,
            message=message,
        )

    @classmethod
    async def get_chat_history_for_room(cls, room_id: str) -> list[MessageToRoomModel]:
        # 채팅방의 이전 채팅 내역을 가져옴.
        chat_history = await cls.filter(room_id=room_id).order_by("created_at").limit(50).all()
        return chat_history
