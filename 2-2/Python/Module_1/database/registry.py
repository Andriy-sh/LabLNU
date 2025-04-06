from Module_1.database.sqlite_db import SQLiteDB


class DatabaseRegistry:
    _databases = {}

    @classmethod
    def register(cls, name, db_instance):
        cls._databases[name] = db_instance

    @classmethod
    def get(cls, name):
        return cls._databases.get(name)


DatabaseRegistry.register("category", SQLiteDB("category"))
DatabaseRegistry.register("user", SQLiteDB("user"))
DatabaseRegistry.register("switch_user", SQLiteDB("switch_user"))
DatabaseRegistry.register("product", SQLiteDB("product"))
