from typing import Generic, TypeVar, TypedDict, Type

T = TypeVar('T', bound=TypedDict)


class BaseGraphQLModel(Generic[T]):

    result_dict: Type[T]

    def __init__(self, result_dict: Type[T]) -> None:
        self.result_dict = result_dict

    def collect_attributes(self):
        for key in self.result_dict.keys():
            self.__dict__[key] = self.result_dict[key]
