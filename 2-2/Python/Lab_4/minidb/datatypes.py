import datetime

class DataType:
    def __init__(self, value):
        self.value = value
        self.validate(value)
    
    def validate(self, value):
        pass
    
    def to_string(self, value):
        pass
        
    def __str__(self):
        return str(self.to_string(self.value))
    
    def __repr__(self):
         return f'{self.__class__.__name__}({self.to_string(self.value)})' 

class IntegerType(DataType):
    def validate(self, value):
        if not isinstance(value, int):
            raise ValueError(f'Value {value} is not an integer')
    
    def to_string(self, value):
        return str(value)

class StringType(DataType):
    def validate(self, value):
        if not isinstance(value, str):
            raise ValueError(f'Value {value} is not a string')
    
    def to_string(self, value):
        return value

class DateType(DataType):
    def validate(self, value):
        if not isinstance(value, datetime.date):
            raise ValueError(f'Value {value} is not a date')
    def to_string(self, value):
        return value.strftime('%Y-%m-%d')

class BooleanType(DataType):
    def validate(self, value):
        if not isinstance(value, bool):
            raise ValueError(f'Value {value} is not a boolean')
    def to_string(self, value):
        return 'true' if value else 'false'