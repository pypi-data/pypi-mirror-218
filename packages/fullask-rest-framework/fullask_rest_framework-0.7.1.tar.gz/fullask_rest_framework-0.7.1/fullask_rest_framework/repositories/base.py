from typing import Generic, TypeVar

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """
    The Base Repository class of all Repositories.
    """
