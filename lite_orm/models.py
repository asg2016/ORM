import sqlite3
from abc import ABCMeta

class Field(metaclass=ABCMeta):
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

    def to_sql(self):
        sql = '{0.local_name} {0.data_type}'.format(self)
        return sql

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
            if isinstance(value, Field) and value.foreign_key == False:
                cls.__fields__[key] = value
                cls.__fields__[key].name = '{}.{}'.format(cls.__table_name__, key)
                cls.__fields__[key].short_name = key
                fields[key] = value.default
            elif isinstance(value, Field) and value.foreign_key == True:
                cls.__fields__['foreign_key'] = value
        return fields


def _get_model_fields(model):
    fields = {}
    for field_name, field_val in model.__dict__.items():
        if not field_name.startswith('__'):
            fields[field_name] = field_val
    return fields


def _is_primary_field(model, field_name):
    return model.__fields__[field_name].primary_key


class Model(metaclass=MetaData):
    def __init__(self, **kwargs):
        self.__dict__.update(self.fields)
        for key, val in kwargs.items():
            self.__dict__.update(val)
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
        sql = '''select name from sqlite_master where type=? and name=?'''
        res = self._exec_sql_(sql, ['table', self.__table_name__])
        print(sql)
        return len(res)>0

    def _exec_sql_(self, sql, params):
        data = None
        if not params is None:
            data = self.__cursor__.execute(sql, params).fetchall()
        else:
            data = self.__cursor__.execute(sql).fetchall()
        self.__connection__.commit()
        # if len(data) == 1:
        #     return data[0]
        return data

    def _create_table_(self):
        sql = 'create table {.__table_name__}('.format(self)
        for field_name, field_instance in self.__fields__.items():
            sql += field_instance.to_sql(True)
        sql = sql[:len(sql)-1] + ');'
        print(sql)
        return self._exec_sql_(sql, None)

    def save(self, method='update'):
        primary_field = None
        sql = ''
        if method.lower() == 'update':
            sql = 'Update {.__table_name__} Set '.format(self)
            for cur_f_name, cur_f_val in self.__fields__.items():
                if _is_primary_field(self, cur_f_name):
                    primary_field = cur_f_name
                    continue
                if isinstance(self.fields[cur_f_name],str):
                    sql += '{0}="{1}" ,'.format(cur_f_name, self.__dict__[cur_f_name])
                else:
                    sql += '{0}={1} ,'.format(cur_f_name, self.__dict__[cur_f_name])
            sql = sql[:len(sql)-1]
            sql += ' where {0}={1}'.format(primary_field, self.__dict__[primary_field])
        elif method.lower() == 'insert':
            sql = 'Insert Into {.__table_name__}('.format(self)
            for cur_f_name, cur_f_val in self.__fields__.items():
                if not _is_primary_field(self, cur_f_name):
                    sql += '{0},'.format(cur_f_name)
            sql = sql[:len(sql) - 1] + ') values ('
            for cur_f_name, cur_f_val in self.__fields__.items():
                if not _is_primary_field(self, cur_f_name):
                    if isinstance(self.fields[cur_f_name], str):
                        sql += '"{0}",'.format(self.__dict__[cur_f_name])
                    else:
                        sql += '{0},'.format(self.__dict__[cur_f_name])
            sql = sql[:len(sql) - 1] + ')'
        return self._exec_sql_(sql, None)


    def _drop_table_(self):
        sql = 'drop table {.__table_name__}'.format(self)
        return self._exec_sql_(sql, None)

    def select(self, **kwargs):
        sql = 'Select * From ' + self.__table_name__
        where = ''
        for key, val in kwargs.items():
            where += ' {0} = {1} '.format(key, val)
        if where != '':
            sql += ' where' + where
        data = self._exec_sql_(sql, None)
        data_models = []
        for values in data:
            model_dict = {}
            for id_val, field in enumerate(self.fields):
                model_dict[field] = values[id_val]
            data_models.append(self.__class__(kwargs=model_dict))
        return data_models


    def _upd_(self):
        pass

    def _ins_(self):
        pass

    def _del_(self):
        pass
