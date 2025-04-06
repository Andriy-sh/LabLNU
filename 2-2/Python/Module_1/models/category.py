from Module_1.models.base_model import BaseModel


class Category(BaseModel):
    fields = {
        "name": "Text",
        "description": "Text",
    }
