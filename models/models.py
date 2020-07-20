from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Links(models.Model):
    """
    The Link model
    """
    id = fields.CharField(max_length=20, pk=True)
    url = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    lifetime = fields.DatetimeField(null=True)
    visits = fields.IntField(default=0)


Link = pydantic_model_creator(Links, name="Link")