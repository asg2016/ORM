from abc import ABCMeta

class Field(metaclass=ABCMeta):
    def __init__(self, name=None, require=False, autoincrement=False,
                 foreign_key=None, nullable=True, max_length=None,
                 primary_key=False, default=None):
        self.name = name
        self.require = require
        self.autoincrement = autoincrement
        self.foreign_key = foreign_key
        self.nullable = nullable
        self.max_length = max_length
        self.primary_key = primary_key
        if isinstance(default, bool):
            self.default = str(default)
        else:
            self.default = default

    def to_sql(self):
        sql = '{0.name} {0.data_type}'.format(self)
        if self.max_length is not None:
            sql += '({0.max_length})'.format(self)
        if self.primary_key:
            sql += ' PRIMARY KEY '
        if self.default:
            sql += ' DEFAULT {0.default}'.format(self)
        if not self.nullable:
            sql += ' NOT NULL '
        if self.autoincrement:
            sql += ' AUTOINCREMENT '
        if self.foreign_key:
            sql += '{}'.format(self.foreign_key.to_sql())
        return sql


class TextField(Field):
    data_type = 'Text'

class IntField(Field):
    data_type = 'Integer'

class RealField(Field):
    data_type = 'Real'

class DateTimeField(Field):
    data_type = 'Text'

class BoolField(Field):
    data_type = 'Text'


if __name__=='__main__':
    t = TextField(name="fuckup", autoincrement=True, nullable=True, max_length=50, primary_key=True, default="text")
    print(t.to_sql())
