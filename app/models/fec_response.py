from typing import List, Generic, TypeVar, TypedDict

from app.models.dicts.fec_pagination_dict import FecPaginationDict

T = TypeVar('T', bound=TypedDict)


class FecResponse(Generic[T]):

    def __init__(self, results: List[T], pagination: FecPaginationDict) -> None:
        self.results = results
        self.pagination = pagination
