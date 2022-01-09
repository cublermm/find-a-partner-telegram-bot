from dataclasses import asdict

import peewee

from find_a_partner.persistence.models.message import NewMessage, Message


def create(new_entity: NewMessage):
    """ create entity """
    return Message.create(**asdict(new_entity))


def update(entity):
    """ update entity """
    entity.save()


def get_non_throw(*query):
    """
    get entity - non throwing variant
    @param query:
    @return: entity or none entity does not exist
    """
    try:
        return Message.get(query)
    except peewee.DoesNotExist:
        return None


def get_by_id(entity_id: int) -> Message:
    """ get entity """
    return Message.get_by_id(entity_id)


def get_by_id_non_throw(entity_id: int) -> Message:
    """ get entity - non throwing variant """
    try:
        return Message.get_by_id(entity_id)
    except peewee.DoesNotExist:
        return None
