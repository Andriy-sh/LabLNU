from Module_1.database.sqlite_db import SQLiteDB


class DatabaseRegistry:
    _databases = {}

    @classmethod
    def register(cls, name, db_instance):
        cls._databases[name] = db_instance

    @classmethod
    def get(cls, name):
        return cls._databases.get(name)


DatabaseRegistry.register("default", SQLiteDB("default"))
DatabaseRegistry.register("test", SQLiteDB("test"))
