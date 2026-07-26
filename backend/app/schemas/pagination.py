from typing import Generic, TypeVar, List

from pydantic import BaseModel


T = TypeVar("T")


class PaginationMeta(BaseModel):
    page: int
    size: int
    total: int


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    meta: PaginationMeta
