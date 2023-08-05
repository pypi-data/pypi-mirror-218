import datetime
import inspect
from collections.abc import Callable
from copy import deepcopy
from typing import (
    Any,
    TypeVar,
)

import fastapi.routing
from fastapi.routing import APIRoute
from starlette._utils import is_async_callable
from starlette.routing import (
    BaseRoute,
)
from starlette.routing import Mount as Mount  # noqa
from typing_extensions import Self

from universi.structure.common import Endpoint, Sentinel
from universi.structure.endpoints import (
    EndpointDidntExistInstruction,
    EndpointExistedInstruction,
    EndpointHadInstruction,
)
from universi.structure.versions import Versions

T = TypeVar("T", bound=Callable[..., Any])


def same_definition_as_in(t: T) -> Callable[[Callable], T]:
    def decorator(f: Callable) -> T:
        return f  # pyright: ignore

    return decorator


def get_route_index(routes: list[BaseRoute], endpoint: Endpoint):
    for index, route in enumerate(routes):
        if isinstance(route, APIRoute) and (
            route.endpoint == endpoint
            or getattr(route.endpoint, "func", None) == endpoint
        ):
            return index
    return None


class APIRouter(fastapi.routing.APIRouter):
    @same_definition_as_in(fastapi.routing.APIRouter.__init__)
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._deleted_routes = []

    # TODO Raise exception if some route was never used in any version even though it was marked with this decorator
    def only_exists_in_older_versions(self, endpoint: T) -> T:
        index = get_route_index(self.routes, endpoint)
        if index is None:
            raise Exception("Route not found")
        self._deleted_routes.append(self.routes.pop(index))
        return endpoint

    def create_versioned_copies(self, versions: Versions) -> dict[datetime.date, Self]:
        router = self
        for route in router.routes + router._deleted_routes:
            if isinstance(route, APIRoute):
                if not is_async_callable(route.endpoint):
                    raise TypeError(
                        "All versioned endpoints must be asynchronous. Contact my author if you disagree. He's ready for proposals",
                    )
                route.endpoint = versions.versioned(route.endpoint)
        routers = {}
        for version in versions.versions:
            routers[version.date] = router
            router = deepcopy(router)
            for version_change in version.version_changes:
                for instruction in version_change.alter_endpoint_instructions:
                    original_route_index = get_route_index(
                        router.routes,
                        instruction.endpoint,
                    )
                    if isinstance(instruction, EndpointDidntExistInstruction):
                        if original_route_index is None:
                            raise Exception(
                                f"Endpoint from {instruction} doesn't exist in new version",
                            )
                        router.routes.pop(original_route_index)
                    elif isinstance(instruction, EndpointExistedInstruction):
                        assert original_route_index is None
                        deleted_route_index = get_route_index(
                            router._deleted_routes,
                            instruction.endpoint,
                        )
                        if deleted_route_index is None:
                            raise Exception(f"Endpoint from {instruction} didn't exist")
                        router.routes.append(
                            router._deleted_routes.pop(deleted_route_index),
                        )
                    elif isinstance(instruction, EndpointHadInstruction):
                        if original_route_index is None:
                            raise Exception(f"Endpoint from {instruction} didn't exist")
                        route = router.routes[original_route_index]
                        for attr_name in instruction.attributes.__dataclass_fields__:
                            attr = getattr(instruction.attributes, attr_name)
                            if attr is not Sentinel:
                                assert getattr(route, attr_name) != attr
                                setattr(route, attr_name, attr)

        return routers


def is_async_callable(obj: Any) -> bool:
    return inspect.iscoroutinefunction(obj) or (
        callable(obj) and inspect.iscoroutinefunction(obj.__call__)
    )
