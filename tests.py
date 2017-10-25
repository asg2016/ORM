from lite_orm import *

class TestModel(Model):
    id = IntField(primary_key=True, default=0)
    text = TextField(nullable=True, default='Empty')
    price = RealField(nullable=True, default=0.0)


if __name__=='__main__':
    test = TestModel()
    test.text = 'Many tests'
    test.price = 19.28
    test.save()