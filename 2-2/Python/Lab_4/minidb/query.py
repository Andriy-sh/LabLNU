from .row import Row

class SimpleQuery:
    def __init__(self, table):
        self.table = table
        self.columns =  None
        self.conditions = []
        self.agg_column = None
    
    def select(self, columns):
        self.columns = columns
        return self
    def where(self, condition):
        self.conditions.append(condition)
        return self
    
    def aggregate(self, column):
        self.agg_column = column
        return self
    
    def aggregate_count(self):
        filtered_rows = self._filter()
        return len(filtered_rows)
    
    def aggregate_sum(self):
        filtered_rows = self._filter()
        total = 0
        for row in filtered_rows:
            val = row[self.agg_column]
            if val is not None and isinstance(val, int):
                total += val
        return total        
    
    def aggregate_avg(self):
        filtered_rows = self._filter()
        values = []
        for row in filtered_rows:
            val = row[self.agg_column]
            if val is not None and isinstance(val, int):
                values.append(val)
        if not values:
            return 0
        return sum(values) / len(values)    
                   
    def _filter(self):
        filtered_rows = []
        for row in self.table:
            matches_all_conditions = True
            for column, operator, value in self.conditions:
                row_value = row[column]
                if operator == '=' and row_value != value:
                    matches_all_conditions = False
                    break
                elif operator == '!=' and row_value == value:
                    matches_all_conditions = False
                    break
                elif operator == '>' and row_value <= value:
                    matches_all_conditions = False
                    break
                elif operator == '<' and row_value >= value:
                    matches_all_conditions = False
            if matches_all_conditions:
                filtered_rows.append(row)
        return filtered_rows
    
    def execute(self):
        result = []
        filtered_rows = self._filter()

        if hasattr(self, 'sort_columns') and self.sort_columns:
            filtered_rows.sort(key=lambda row: row[self.sort_columns] if row[self.sort_columns] is not None else '', reverse=not self.sort_ascending)
        for row in filtered_rows:
            if self.columns:
                new_row = {column: row[column] for column in self.columns if column in row.keys()}
                result.append(Row(new_row))
            else:
                result.append(row)
        return result

class JoinedTable:
    def __init__(self, table1, table2, column1, column2):
        self.table1 = table1
        self.table2 = table2
        self.column1 = column1
        self.column2 = column2
        self.joined_rows = []
        self._join()
        
    def _join(self):
        for row1 in self.table1:
            for row2 in self.table2:
                if row1[self.column1] == row2[self.column2]:
                    joined_data = {}
                    for k, v in row1.data.items():
                        joined_data[k] = v
                    for k, v in row2.data.items():
                        joined_data[k] = v

                    joined_columns = list(self.table1.columns.values()) + list(self.table2.columns.values())
                    row_obj = Row(joined_columns)
                    for key, value in joined_data.items():
                        row_obj[key] = value
                    self.joined_rows.append(row_obj)
    def __iter__(self):
        return iter(self.joined_rows)