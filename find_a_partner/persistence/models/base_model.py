"""
database configuration
"""

from peewee import *

db = SqliteDatabase('find_a_partner_db.db')
VERSION = 1


class BaseModel(Model):
    class Meta:
        database = db
