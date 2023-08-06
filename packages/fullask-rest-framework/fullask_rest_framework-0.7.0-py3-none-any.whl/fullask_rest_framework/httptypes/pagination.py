from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


@dataclass
class PaginationResponse(Generic[T]):
    count: Optional[int]
    next_page: Optional[int]
    previous_page: Optional[int]
    results: List


@dataclass
class PaginationRequest:
    page: Optional[int] = None
    per_page: Optional[int] = None
