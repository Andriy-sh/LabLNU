class DataType:
    def validate(self, value):
        raise NotImplementedError

    def __str__(self):
        return self.__class__.__name__


class IntegerType(DataType):
    def validate(self, value):
        return isinstance(value, int)


class StringType(DataType):
    def __init__(self, max_length=None):
        self.max_length = max_length

    def validate(self, value):
        if not isinstance(value, str):
            return False
        if self.max_length and len(value) > self.max_length:
            return False
        return True


class BooleanType(DataType):
    def validate(self, value):
        return isinstance(value, bool)


class DateType(DataType):
    def validate(self, value):
        # Припустимо, що дата передається у форматі рядка "YYYY-MM-DD"
        try:
            from datetime import datetime
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except ValueError:
            return False
