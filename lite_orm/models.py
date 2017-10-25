import sqlite3
from abc import ABCMeta

class Field(metaclass=ABCMeta):
    def __init__(self, name=None, require=False,
                 foreign_key=None, nullable=True, max_length=None,
                 primary_key=False, default=None):
        self.name = name
        self.require = require
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
            sql += ' primary key'
        if self.default:
            sql += ' default {0.default}'.format(self)
        if not self.nullable:
            sql += ' not null'
        else:
            sql += ' null'
        if self.foreign_key:
            sql += '{}'.format(self.foreign_key.to_sql())
        sql += ','
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
        cls.__fields__ = {}
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
                cls.__fields__[key] = value
                fields[key] = value.default
        return fields


class Model(metaclass=MetaData):
    def __init__(self, **kwargs):
        self.__dict__.update(self.fields)
        for key, val in kwargs.items():
            setattr(self, key, val)
        self._connect_()
        if not self._table_exists_():
            self._create_table_()

    def __del__(self):
        if self.__connection__:
            self._close_()

    def _connect_(self):
        self.__connection__ = sqlite3.connect(self.__db__)
        self.__cursor__ = self.__connection__.cursor()

    def _close_(self):
        self.__connection__.commit()
        self.__cursor__.close()
        self.__connection__.close()

    def _table_exists_(self):
        sql = '''SELECT name FROM sqlite_master WHERE type=? AND name=?'''
        res = self._exec_sql_(sql, ['table', self.__table_name__])
        return len(res)>0

    def _exec_sql_(self, sql, params):
        data = None
        if not params is None:
            data = self.__cursor__.execute(sql, params).fetchall()
        else:
            self.__cursor__.execute(sql)
            data = True
        return data

    def _create_table_(self):
        sql = 'CREATE TABLE {.__table_name__}('.format(self)
        for field_name, field_instance in self.__fields__.items():
            sql += field_instance.to_sql()
        sql = sql[:len(sql)-1] + ');'
        return self._exec_sql_(sql, None)

    def save(self):
        if self.

    def _drop_table_(self):
        sql = 'DROP TABLE {.__table_name__}'.format(self)
        return self._exec_sql_(sql, None)

    def select(self):
        pass

    def _upd_(self):
        pass

    def _ins_(self):
        pass

    def _del_(self):
        pass
