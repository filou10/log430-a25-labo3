import graphene
from graphene import Int, ObjectType, String

from db import get_redis_conn
from stocks.schemas.product import Product


class Query(ObjectType):
    product = graphene.Field(Product, product_id=String(required=True))
    stock_level = Int(product_id=String(required=True))

    def resolve_product(self, info, product_id):
        """Create an instance of Product based on stock info for that product that is in Redis"""
        redis_client = get_redis_conn()
        product_data = redis_client.hgetall(f"stock:{product_id}")

        if product_data:
            return Product(
                id=product_id,
                name=product_data.get("name"),
                sku=product_data.get("sku"),
                quantity=int(product_data.get("quantity")),
                price=float(product_data.get("price", -1)),
            )
        return None

    def resolve_stock_level(self, info, product_id):
        """Retrieve stock quantity from Redis"""
        redis_client = get_redis_conn()
        quantity = redis_client.hget(f"stock:{product_id}", "quantity")
        return int(quantity) if quantity else 0
