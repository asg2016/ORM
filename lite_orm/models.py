class MetaModel(type):

    def __init__(cls, name, bases, attr_dict):
        table_name = attr_dict.get('__tablename__')

