class Row:
    _id_counter = 1  

    def __init__(self, columns):
        self.columns = {col.name: col for col in columns}
        self.id = Row._id_counter  
        Row._id_counter += 1  
        self.data = {}

    def __setitem__(self, key, value):
        if key not in self.columns:
            raise ValueError(f'Column {key} does not exist')
        self.columns[key].validate_type(value)
        self.data[key] = value

    def __getitem__(self, key):
        return self.data.get(key)

    def __str__(self):
        return f'Row ID: {self.id}, Data: {self.data}'
    
    def __eq__(self, other):
        if not isinstance(other, Row):
            return False
        return self.data == other.data  

    
    def __ne__(self, other):
        return not self.__eq__(other)