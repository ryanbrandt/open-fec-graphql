import json
from typing import Any, List


class FecResponse():
    class FecPagination():
        def __init__(self, page: int, count: int, pages: int, per_page: int) -> None:
            self.page = page
            self.count = count
            self.pages = pages
            self.per_page = per_page

    def __init__(self, results: List[Any], pagination: json) -> None:
        self.results = results
        self.pagination = FecResponse.FecPagination(
            pagination['page'], pagination['count'], pagination['pages'], pagination['per_page'])
