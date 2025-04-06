from Module_1.models.product import Product


def create_product(data):
    return Product.create(**data)


def get_product(product_id):
    return Product.get(product_id)


def get_product_by_category_id(category_id):
    return Product.filter_by_field("category_id", category_id)
