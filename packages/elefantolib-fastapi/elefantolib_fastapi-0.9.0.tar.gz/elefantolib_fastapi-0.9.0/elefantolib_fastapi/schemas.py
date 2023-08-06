from typing import TypeVar

from pydantic import BaseModel
from pydantic.generics import Generic


M = TypeVar('M')


class PaginatedResponse(BaseModel, Generic[M]):
    count: int
    pages: int
    results: list[M]
