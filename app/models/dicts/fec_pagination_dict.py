from typing import TypedDict


class FecPaginationDict(TypedDict):
    page: str
    count: int
    pages: int
    per_page: int
