from typing import TypedDict


class FecPaginationDict(TypedDict):
    page: int
    count: int
    pages: int
    per_page: int
