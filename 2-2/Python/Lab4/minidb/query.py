from .row import Row
class SimpleQuery:
    def __init__(self, table):
        self.table = table
        self.selected_columns = None
        self.filter_conditions = []

    def select(self, columns):
        self.selected_columns = columns
        return self

    def where(self, column, operator, value):
        self.filter_conditions.append((column, operator, value))
        return self

    def order_by(self, column, ascending=True):
        self.sort_column = column
        self.sort_ascending = ascending
        return self

    def execute(self):
        results = []
        filtered_rows = []

        # Фільтрація рядків за умовами where
        for row in self.table:
            matches_all_conditions = True
            for column, operator, value in self.filter_conditions:
                row_value = row[column]
                if operator == "=" and row_value != value:
                    matches_all_conditions = False
                    break
                elif operator == ">" and not (row_value > value):
                    matches_all_conditions = False
                    break
                elif operator == "<" and not (row_value < value):
                    matches_all_conditions = False
                    break
                elif operator == ">=" and not (row_value >= value):
                    matches_all_conditions = False
                    break
                elif operator == "<=" and not (row_value <= value):
                    matches_all_conditions = False
                    break
            if matches_all_conditions:
                filtered_rows.append(row)

        # Сортування результатів, якщо вказано
        if hasattr(self, 'sort_column') and self.sort_column:
            filtered_rows.sort(
                key=lambda r: r[self.sort_column] if r[self.sort_column] is not None else "",
                reverse=not self.sort_ascending
            )

        # Вибираємо тільки потрібні стовпці
        for row in filtered_rows:
            if self.selected_columns:
                new_row_data = {col: row[col] for col in self.selected_columns if col in row.data}
                results.append(Row(new_row_data))
            else:
                results.append(row)
        return results