from Module_1.models.base_model import BaseModel


class Product(BaseModel):
    fields = {
        "name": "TEXT",
        "price": "NUMERIC",
        "quantity": "NUMERIC",
        "category_id": "NUMERIC",
    }
