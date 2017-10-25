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

class MetaData(type):
    def __init__(cls, name, bases, attr_dict):
        cls.__set_attr__('__table_name__', attr_dict, cls.__name__)
        cls.__set_attr__('__db__', attr_dict, 'base.db')
        cls.fields = cls.__set_fields__(attr_dict)

    def __set_attr__(cls, attr, attr_dict, def_val):
        if attr in attr_dict:
            setattr(cls, attr, attr_dict[attr])
        else:
            setattr(cls, attr, def_val)

    def __set_fields__(cls, attr_dict):
        fields = {}
        for key, value in attr_dict.items():
            if isinstance(value, Field):
                fields[key] = value.default
        return fields


class Model(metaclass=MetaData):
    def __init__(self, **kwargs):
        self.__dict__.update(self.fields)
        for key, val in kwargs.items():
            setattr(self, key, val)

    def _sel_(self):
        pass

    def _upd_(self):
        pass

    def _ins_(self):
        pass

    def _del_(self):
        pass
