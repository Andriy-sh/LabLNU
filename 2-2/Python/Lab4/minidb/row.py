class Row:
    def __init__(self, data):
        self.data = data
        self.id = None

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __eq__(self, other):
        return self.data == other.data

    def __str__(self):
        return f"Row(id={self.id}, data={self.data})"