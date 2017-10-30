from lite_orm import *


class Category(Model):
    id = IntField(primary_key=True)
    text = TextField(nullable=True, default='New category')

    def __str__(self):
        return  self.text


class Goods(Model):
    id = IntField(primary_key=True)
    title = TextField(nullable=True, max_length=100)
    content = TextField(nullable=True, max_length=500)
    option1 = TextField(nullable=True)
    option2 = TextField(nullable=True)
    option3 = TextField(nullable=True)
    price = RealField(nullable=False, default=0)
    category = ForeignKey(model=Category)

    def __str__(self):
        return self.title


if __name__=='__main__':
    g = Goods()
