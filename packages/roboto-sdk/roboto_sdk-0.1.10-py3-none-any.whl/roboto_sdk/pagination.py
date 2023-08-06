import dataclasses
from typing import Generic, Optional, TypeVar

Model = TypeVar("Model")


@dataclasses.dataclass
class PaginatedList(Generic[Model]):
    items: list[Model]
    next_token: Optional[dict[str, str]] = None
