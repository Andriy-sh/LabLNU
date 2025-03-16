class Column:
    def __init__(self, name, data_type, nullable=True):
        self.name = name
        self.data_type = data_type
        self.nullable = nullable

    def validate(self, value):
        if value is None:
            return self.nullable
        return self.data_type.validate(value)

    def __str__(self):
        return f"Column(name={self.name}, type={self.data_type}, nullable={self.nullable})"