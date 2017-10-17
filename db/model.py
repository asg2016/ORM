class Model(object):
    __tablename__ = 'table'
    def __init__(self):
        for key, value in self.__dict__.items():
            pass

class ModelField(object):
    value = None
    def __init__(self, require=False, autoincrement=False, foreign=False, not_null=False):
        self.require = require
        self.autoincrement = autoincrement
        self.foreign = foreign
        self.not_null = not_null

class ForeignKey(ModelField):
    pass

class TextField(ModelField):
    def __init__(self, require=False, not_null=False, max_length=0):
        super().__init__(require=require, not_null=not_null)
        self.max_length=max_length
        self.value = ''

    def get_type(self):
        field_type = 'Text'
        if self.max_length > 0:
            field_type = ''.join(['String','(',self.max_length,')'])
        return field_type

class IntField(ModelField):
    pass

class RealField(ModelField):
    pass

class BoolField(ModelField):
    pass
