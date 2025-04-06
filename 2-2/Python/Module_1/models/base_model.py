from Module_1.database.registry import DatabaseRegistry


class BaseModel:
    _db_instance = DatabaseRegistry.get("default")

    @classmethod
    def use_db(cls, db_name):
        db = DatabaseRegistry.get(db_name)
        if db:
            cls._db_instance = db
        else:
            raise ValueError("DB not found")

    @classmethod
    def create(cls, **data):
        cls._db_instance.create_table(cls.__name__, cls.fields)
        return cls._db_instance.create(cls.__name__, data)

    @classmethod
    def get(cls, obj_id):
        return cls._db_instance.get(cls.__name__, obj_id)

    @classmethod
    def update(cls, obj_id, **data):
        return cls._db_instance.update(cls.__name__, obj_id, data)

    @classmethod
    def delete(cls, obj_id):
        return cls._db_instance.delete(cls.__name__, obj_id)
