from dataclasses import dataclass
from enum import Enum
import datetime

from peewee import *

from find_a_partner.persistence.models.base_model import BaseModel
from find_a_partner.persistence.models.user import User
from find_a_partner.persistence.pee_wee_helper import IntEnumField


@dataclass
class NewMessage:
    content: str
    user: User


class Message(BaseModel):
    accepted = BooleanField(default=False)
    user = ForeignKeyField(User, backref='messages')
    # TODO: use correct message content length
    content = CharField()
    created_date = DateTimeField(default=datetime.datetime.now)
