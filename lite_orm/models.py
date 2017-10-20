class MetaModel(type):
    def __init__(cls):
        print(cls.__class__)

class Model(MetaModel):
    def __init__(self, **kwargs):
        pass



class TestModel(Model):
    pass
    # id = IntField(name='id', require=True, autoincrement=True, primary_key=True)
    # text = TextField(name='mytext', nullable=True, default='Empty')


if __name__=='__main__':
    test = TestModel()
