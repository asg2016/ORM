from lite_orm import *

class TestModel(Model):
    id = IntField(name='id', primary_key=True, default=0)
    text = TextField(name='mytext', nullable=True, default='Empty')
    price = RealField(name='price', nullable=True, default=0.0)


if __name__=='__main__':
    test = TestModel()
    test.text = 'Many tests'
    price = 19.25
