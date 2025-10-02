from graphene import Float, Int, ObjectType, String


class Product(ObjectType):
    id = Int()
    name = String()
    sku = String()
    price = Float()
    quantity = Int()
