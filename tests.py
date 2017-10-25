from lite_orm import *

class TestModel(Model):
    id = IntField(name='id', primary_key=True, default=0)
    text = TextField(name='mytext', nullable=True, default='Empty')
    price = RealField(name='price', nullable=True, default=0.0)


if __name__=='__main__':
    test = TestModel()
    print(test.id)
    print(test.text)
    print(test.price)