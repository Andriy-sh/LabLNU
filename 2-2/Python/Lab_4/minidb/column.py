from .datatypes import IntegerType, StringType, BooleanType, DateType

class Column:
    def __init__(self, name, data_type, nullable=False):
        self.name = name
        self.data_type = data_type
        self.nullable = nullable
    
    @classmethod
    def form_string(cls, string):
        try:
            name, data_type, nullable = string.split()

            data_types = {
                "IntegerType": IntegerType,
                "StringType": StringType,
                "BooleanType": BooleanType,
                "DateType": DateType
            }

            if data_type not in data_types:
                raise ValueError(f"Unsupported data type: {data_type}")
        
            return cls(name, data_types[data_type](), nullable)
        except ValueError:
            raise ValueError(f'Invalid column string: {string}')
            
        
    def validate_type(self, value):
        if value is not None or not self.nullable:  
            try:
                self.data_type.validate(value)
            except ValueError as e:
                raise ValueError(f'Column {self.name}: {e}')
    def __str__(self):
        return f'{self.name} ({self.data_type.__class__.__name__})'