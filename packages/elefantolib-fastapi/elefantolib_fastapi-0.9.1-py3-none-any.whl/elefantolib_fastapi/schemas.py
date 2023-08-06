from typing import Generic, TypeVar

from pydantic import BaseModel


M = TypeVar('M')


class PaginatedResponse(BaseModel, Generic[M]):
    count: int
    pages: int
    results: list[M]
