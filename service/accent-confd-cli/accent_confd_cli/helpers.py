# Copyright 2023 Accent Communications


class ListBuildingMixin:
    _columns = []
    _removed_columns = []

    def extract_column_headers(self, item):
        headers = item.keys()
        missing_columns = set(headers) - set(self._columns) - set(self._removed_columns)
        columns = self._columns + list(missing_columns)
        return columns

    def extract_items(self, headers, items):
        results = []
        for item in items:
            result = [item[header] for header in headers]
            results.append(result)
        return results
