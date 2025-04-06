from Module_1.models.base_model import BaseModel


class User(BaseModel):
    fields = {
        "name": "TEXT",
        "email": "TEXT"
    }
