from peewee import *

from find_a_partner.persistence.models.base_model import db
from find_a_partner.persistence.models.message import Message
from find_a_partner.persistence.models.user import User
from find_a_partner.persistence.models.version import Version, check_set_version


def initialize():
    """
    initialize database
    - create tables if necessary
    - handle database migration
    """
    db.connect()
    db.create_tables([User, Version, Message])
    check_set_version()


def tear_down():
    """
    close database
    """
    db.close()