from dataclasses import dataclass
from enum import Enum
import datetime

from peewee import *

from find_a_partner.persistence.models.base_model import BaseModel
from find_a_partner.persistence.pee_wee_helper import IntEnumField


class TrustedState(Enum):
    UNDEFINED = 1
    NOT_TRUSTED = 2
    TRUSTED = 3


class UserLevel(Enum):
    USER = 1
    ADMIN = 2


@dataclass
class NewUser:
    telegram_id: int
    username: str
    # first_name: str | None
    # last_name: str | None
    trusted_state: TrustedState = TrustedState.UNDEFINED


class User(BaseModel):
    telegram_id = IntegerField(unique=True)
    trusted_state = IntEnumField(choices=TrustedState, default=TrustedState.UNDEFINED)
    trusted_reason = CharField(null=True)
    user_level = IntEnumField(choices=UserLevel, default=UserLevel.USER)
    created_date = DateTimeField(default=datetime.datetime.now)
    username = CharField()
    # first_name = CharField(null=True)
    # last_name = CharField(null=True)