from peewee import IntegerField

class IntEnumField(IntegerField):
    """
    This class enable a Enum like field for Peewee
    """
    def __init__(self, choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = choices

    def db_value(self, enum):
        return enum.value

    def python_value(self, value):
        return self.choices(value)
