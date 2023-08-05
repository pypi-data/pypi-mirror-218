import abc
import datetime
import functools
from collections.abc import Callable, Collection, Sequence
from typing import Any, ParamSpec, TypeAlias, TypeVar, overload

from fastapi.routing import _prepare_response_content

from universi.header import api_version_var
from universi.structure.endpoints import AlterEndpointSubInstruction

from .common import Endpoint
from .responses import AlterResponseInstruction
from .schemas import AlterSchemaInstruction

_P = ParamSpec("_P")
_R = TypeVar("_R")
Date: TypeAlias = str


class AbstractVersionChange(abc.ABC):
    side_effects: bool
    description: str
    alter_schema_instructions: Sequence[AlterSchemaInstruction]
    alter_endpoint_instructions: Sequence[AlterEndpointSubInstruction]
    alter_response_instructions: dict[Endpoint, AlterResponseInstruction]

    def __init_subclass__(
        cls,
        *,
        side_effects: bool = False,
        description: str,
        alter_instructions: Collection[
            AlterSchemaInstruction | AlterEndpointSubInstruction
        ] = (),
    ) -> None:
        cls.side_effects = side_effects
        cls.description = description
        cls.alter_schema_instructions = []
        cls.alter_endpoint_instructions = []
        for alter_instruction in alter_instructions:
            if isinstance(alter_instruction, AlterSchemaInstruction):
                cls.alter_schema_instructions.append(alter_instruction)
            else:
                cls.alter_endpoint_instructions.append(alter_instruction)
        cls.alter_response_instructions = {
            instruction.endpoint: instruction
            for instruction in cls.__dict__.values()
            if isinstance(instruction, AlterResponseInstruction)
        }
        repetitions = set()
        for alter_instruction in cls.alter_schema_instructions:
            assert (
                alter_instruction.schema not in repetitions
            ), f"Model {alter_instruction.schema} got repeated. Please, merge these instructions."
            repetitions.add(alter_instruction.schema)

    def __init__(self) -> None:
        raise TypeError(
            f"Can't instantiate {self.__class__.__name__} as it was never meant to be instantiated.",
        )


class Version:
    def __init__(
        self,
        date: datetime.date,
        *version_changes: type[AbstractVersionChange],
    ) -> None:
        self.date = date
        self.version_changes = version_changes


class Versions:
    def __init__(self, *versions: Version) -> None:
        self.versions = versions
        if sorted(versions, key=lambda v: v.date, reverse=True) != list(versions):
            raise ValueError(
                "Versions are not sorted correctly. Please sort them in descending order.",
            )
        self.versioned_schemas = {
            instruction.schema.__module__
            + instruction.schema.__name__: instruction.schema
            for version in self.versions
            for version_change in version.version_changes
            for instruction in version_change.alter_schema_instructions
        }

    # TODO: It might need caching for iteration to speed it up
    def data_to_version(
        self,
        endpoint: Endpoint,
        data: dict[str, Any],
        version: datetime.date,
    ) -> dict[str, Any]:
        for v in self.versions:
            if v.date <= version:
                break
            for version_change in v.version_changes:
                if endpoint in version_change.alter_response_instructions:
                    version_change.alter_response_instructions[endpoint](data)

        return data

    @overload
    def versioned(self, endpoint: Endpoint[_P, _R]) -> Endpoint[_P, _R]:
        ...

    @overload
    def versioned(
        self,
        endpoint: None = None,
    ) -> Callable[[Endpoint[_P, _R]], Endpoint[_P, _R]]:
        ...

    def versioned(
        self,
        endpoint: Endpoint | None = None,
    ) -> Callable[[Endpoint[_P, _R]], Endpoint[_P, _R]] | Endpoint[_P, _R]:
        if endpoint is not None:

            @functools.wraps(endpoint)
            async def decorator(*args: _P.args, **kwargs: _P.kwargs) -> _R:
                return await self._convert_endpoint_response_to_version(
                    endpoint,
                    args,
                    kwargs,
                )

            decorator.func = endpoint
            return decorator

        def wrapper(endpoint: Endpoint[_P, _R]) -> Endpoint[_P, _R]:
            @functools.wraps(endpoint)
            async def decorator(*args: _P.args, **kwargs: _P.kwargs) -> _R:
                return await self._convert_endpoint_response_to_version(
                    endpoint,
                    args,
                    kwargs,
                )

            decorator.func = endpoint
            return decorator

        return wrapper

    async def _convert_endpoint_response_to_version(
        self,
        endpoint: Endpoint,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> Any:
        response = await endpoint(*args, **kwargs)
        api_version = api_version_var.get()
        if api_version is None:
            return response
        # TODO We probably need to call this in the same way as in fastapi instead of hardcoding exclude_unset.
        # We have such an ability if we force passing the route into this wrapper. Or maybe not... Important!
        response = _prepare_response_content(response, exclude_unset=False)
        return self.data_to_version(endpoint, response, api_version)
