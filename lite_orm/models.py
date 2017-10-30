import sqlite3
from .helpers import _get_model_fields, _is_primary_field
from .query import Connection


class MetaData(type):
    __fields__ = {}
    def __init__(cls, name, bases, attr_dict):
        cls.__set_attr__('__table_name__', attr_dict, cls.__name__)
        for field, field_ins in attr_dict.items():

        # cls.__connection__ = Connection(cls, 'base.db',cls.__table_name__)
        # cls.__set_attr__('__db__', attr_dict, 'base.db')
        # cls
        # cls.__fields__ = _get_model_fields(cls)

    def __set_attr__(cls, attr, attr_dict, def_val):
        if attr in attr_dict:
            setattr(cls, attr, attr_dict[attr])
        else:
            setattr(cls, attr, def_val)

class Model(metaclass=MetaData):
    def __init__(self, **kwargs):
        self.__dict__.update(self.fields)
        print(kwargs)
        for key, val in kwargs.items():
            if val['__qualname__'] == self.__class__.__name__:
                self.__dict__.update(val)
        # self._connect_()
        # if not self._table_exists_():
        #     self._create_table_()

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

