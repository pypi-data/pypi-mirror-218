import inspect
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, ParamSpec, cast

from .common import Endpoint

_P = ParamSpec("_P")


@dataclass
class AlterResponseInstruction:
    endpoint: Endpoint
    method: Callable[[dict[str, Any]], None]

    def __post_init__(self):
        assert inspect.signature(self.method).return_annotation is None
        assert len(inspect.signature(self.method).parameters) == 1
        annotation = inspect.signature(self.method).parameters["data"].annotation
        assert annotation == dict[str, Any], annotation

    def __call__(self, data: dict[str, Any]) -> None:
        return self.method(data)


def alter_response(endpoint: Endpoint) -> "type[staticmethod[_P, None]]":
    return cast(type[staticmethod], lambda f: AlterResponseInstruction(endpoint, f))
