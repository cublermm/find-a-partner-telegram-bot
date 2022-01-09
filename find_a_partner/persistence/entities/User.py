from dataclasses import asdict

import peewee

from find_a_partner.persistence.db import db
from find_a_partner.persistence.models.user import NewUser, User, UserLevel, TrustedState


def create(new_entity: NewUser):
    """ create entity """
    return User.create(**asdict(new_entity))


def upsert(new_entity: NewUser):
    """ get or create entity """
    with db.atomic():
        user, created = User.get_or_create(telegram_id=new_entity.telegram_id, username=new_entity.username)
        user.update(**asdict(new_entity))


def update(entity):
    """ update entity """
    entity.save()


def get_by_id(entity_id: int) -> User:
    """ get entity """
    return User.get_by_id(entity_id)


def get_non_throw(*query):
    """
    get entity - non throwing variant
    @param query:
    @return: entity or none entity does not exist
    """
    try:
        return User.get(query)
    except peewee.DoesNotExist:
        return None


def get_by_telegram_id(telegram_id):
    """ get entity by telegram id """
    return get_non_throw(User.telegram_id == telegram_id);


def get_by_username(username):
    """ get entity by username """
    return get_non_throw(User.username == username)


def get_all_admins() -> [User]:
    """
    get all admins
    @return:
    """
    return User.select().where(User.user_level == UserLevel.ADMIN)


def get_all_trusted_users() -> [User]:
    """
    get all trusted users
    @return:
    """
    return User.select().where(User.trusted_state == TrustedState.TRUSTED)
