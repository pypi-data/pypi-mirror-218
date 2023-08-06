from typing import Generic, TypeVar

from pydantic.generics import GenericModel


M = TypeVar('M')


class PaginatedResponse(GenericModel, Generic[M]):
    count: int
    pages: int
    results: list[M]
