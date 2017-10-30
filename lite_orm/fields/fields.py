from abc import ABCMeta


class Field(metaclass=ABCMeta):
    __table_name__ = None
    def __init__(self, require=False,
                 nullable=True, max_length=None,
                 primary_key=False, default=None):
        self.require = require
        self.foreign_key = False
        self.nullable = nullable
        self.max_length = max_length
        self.primary_key = primary_key
        self.default = default

    def to_sql(self, create=False):
        if create:
            sql = '{0.short_name} {0.data_type}'.format(self)
        else:
            sql = '{0.name} {0.data_type}'.format(self)
        if self.max_length is not None:
            sql += '({0.max_length})'.format(self)
        if self.primary_key:
            sql += ' primary key'
        sql += ' default "{0.default}"'.format(self)
        if not self.nullable:
            sql += ' not null'
        else:
            sql += ' null'
        if self.foreign_key:
            sql += '{}'.format(self.foreign_key.to_sql())
        sql += ','
        return sql


class TextField(Field):
    data_type = 'text'

class IntField(Field):
    data_type = 'integer'

class RealField(Field):
    data_type = 'real'

class ForeignKey(Field):
    data_type = 'integer'
    def __init__(self, model=None):
        self.model = model()
        self.short_name = 'id'
        self.name = '{}.{}'.format(model.__table_name__,'id')
        self.local_name = '{}_{}'.format(model.__table_name__.lower(),'id')
        self.join_table = model.__table_name__
        self.foreign_key = True

    def to_sql(self, create=False):
        if create:
            sql = '{0.local_name} {0.data_type}'.format(self)
        else:
            sql = '{0.local_name} {0.data_type}'.format(self)
        return sql