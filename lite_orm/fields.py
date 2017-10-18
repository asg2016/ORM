from abc import ABCMeta

class Field(metaclass=ABCMeta):
    def __init__(self, name=None, require=False, autoincrement=False,
                 foreign_key=False, nullable=True, max_length=None,
                 primary_key=False, default=None):
        self.name = name
        self.require = require
        self.autoincrement = autoincrement
        self.foreign_key = foreign_key
        self.nullable = nullable
        self.max_length = max_length
        self.primary_key = primary_key
        self.default = default

    def to_sql(self):
        sql = '{0.name} {0.data_type}'.format(self)
        if self.max_length is not None:
            sql += '({0.max_length})'.format.self
        if self.primary_key:
            sql += ' PRIMARY KEY '
        if self.default:
            sql += ' DEFAULT {0.default}'.format(self)
        if not self.nullable:
            sql += ' NOT NULL '
        if self.autoincrement:
            sql += ' AUTOINCREMENT '
        if self.foreign_key:
            pass



class ForeignKey(Field):
    def __init__(self, autoincrement=True):
        super().__init__(require=True, autoincrement=autoincrement, foreign_key=True)


class TextField(Field):
    def __init__(self, require=False, nullable=False, max_length=0):
        super().__init__(require=require, nullable=nullable)
        self.max_length=max_length
        self.value = ''

    def get_type(self):
        field_type = 'Text'
        if self.max_length > 0:
            field_type = ''.join(['String','(',self.max_length,')'])
        return field_type

class IntField(Field):
    def __init__(self, require=False, nullable=False):
        super().__init__(require=require, nullable=nullable)

class RealField(Field):
    pass

class BoolField(Field):
    pass
