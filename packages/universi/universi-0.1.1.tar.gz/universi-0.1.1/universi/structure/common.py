from collections.abc import Awaitable, Callable
from typing import Any, ParamSpec, TypeAlias, TypeVar

from pydantic import BaseModel

Sentinel: Any = object()
VersionedModel = BaseModel
VersionDate = str
_P = ParamSpec("_P")
_R = TypeVar("_R")
Endpoint: TypeAlias = Callable[_P, Awaitable[_R]]
