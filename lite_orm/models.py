class MetaData(type):
    def __init__(cls, name, bases, attr_dict):
        pass


class Model(MetaData):
    pass



class TestModel(Model):
    pass
    # id = IntField(name='id', require=True, autoincrement=True, primary_key=True)
    # text = TextField(name='mytext', nullable=True, default='Empty')


if __name__=='__main__':
    test = TestModel()
