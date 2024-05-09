from tortoise import fields


class Common:
    id = fields.IntField(pk=True, max_length=40)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
