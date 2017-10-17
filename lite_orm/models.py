from . import fields


class MetaModel(type):

    def __init__(cls, *args, **kwargs):
        if cls.__table_name__ == '':
            cls.__table_name__ = cls.__name__
        cls.__build_model()

    def __build_model(cls):
        for key, value in cls.__dict__.items():
            if not key.startswith('__') and value.__class__.__name__.endswith('Field'):
                if value.data_type == 'int':
                    cls.__dict__.pop(key,0)
                    cls.__dict__.update(key=key,value=0)



class Model(object, metaclass=MetaModel):
    __table_name__ = ''
    __database__ = ''
    __connection__ = None
    __primary_key__ = None
    __autoincrement__ = True


class TestModel(Model):
    id = fields.IntField()


if __name__=='__main__':
    t = TestModel()
    print(t.__dict__)
