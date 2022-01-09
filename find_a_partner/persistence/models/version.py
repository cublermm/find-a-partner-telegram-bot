from peewee import IntegerField

from find_a_partner.persistence.models.base_model import BaseModel, VERSION


class Version(BaseModel):
    version = IntegerField()


def check_set_version():
    """
    set database version (if not already set)
    check if database version supported by current app version
    """

    # check if db version set
    version = Version.select()
    if len(version) == 0:
        # no db version set => set
        Version.create(version=VERSION)
        return

    # db version set => check if db version supported by current app version
    if version[0].version != VERSION:
        raise Exception('database version not supported by app')

