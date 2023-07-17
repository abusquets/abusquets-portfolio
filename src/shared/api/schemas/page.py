from enum import IntEnum
from typing import Generic, List, Type, TypeVar

from pydantic import BaseModel, Field


class PageSize(IntEnum):
    x100 = 100
    x250 = 250
    x500 = 500
    x1000 = 1000


class PageParams(BaseModel):
    page: int = Field(1, ge=1, description='Page number')
    size: PageSize = PageSize.x500

    class Config:
        use_enum_values = True


T = TypeVar('T')


class PagedResponseSchema(BaseModel, Generic[T]):
    total: int
    page: int
    size: int
    results: List[T]
