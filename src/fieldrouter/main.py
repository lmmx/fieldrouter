from typing import Annotated, Any, TypeVar, Union

from pydantic import BaseModel, BeforeValidator, TypeAdapter, model_validator

__all__ = ("Route", "Routing", "RoutingModel")

RoutePart = Union[int, str]
rp_ta = TypeAdapter(RoutePart)


def split_route(route: str) -> list[RoutePart]:
    """Split a `.`-separated string/integer subpath up into a list."""
    match route:
        case str():
            return list(map(rp_ta.validate_strings, route.split(".")))
        case list():
            return route
        case _:
            raise ValueError(f"Invalid route: {route}")


Route = Annotated[list[RoutePart], BeforeValidator(split_route)]
"""The `.`-separated string keys and integers that specify a JSON-like subpath."""


class Via:
    routes: Route | list[Route]

    def __init__(self, routes):
        self.routes = routes

    def __repr__(self):
        return f"Via(routes={self.routes})"


T = TypeVar("T")


def Routing(tp: T, *, via: str) -> Annotated[T, Via]:
    return Annotated[tp, Via(routes=[via])]


def extract_subpath(path: Route, data: dict) -> Any:
    """Extract a subpath or else an error reporter fallback indicating where it failed."""
    for part_idx, part in enumerate(path):
        reporter = ValueError(f"Missing {part=} on {path}")
        match part:
            case str() as key:
                data = data.get(key, reporter)
            case int() as idx:
                data = (
                    data[idx]
                    if isinstance(data, list) and 0 <= idx < len(data)
                    else reporter
                )
        if data is reporter:
            break
    return data


class RoutingModel(BaseModel):
    """A model which should be subclassed to specify fields at the associated routes.

    ```py
    from typing import Annotated
    from fieldrouter.v2 import Route, RoutingModel


    class DataRouter(RoutingModel):
        some_value: Annotated[int, Route("example.subpath.0")]


    data = {"example": {"subpath": [100]}}
    result = DataRouter.model_validate(data).some_value  # 100
    ```
    """

    @model_validator(mode="before")
    def supply_routes(cls, data: dict):
        values = {}
        for field, route_meta in cls.model_fields.items():
            match route_meta.metadata:
                case [Via()]:
                    route_string = route_meta.metadata[0].routes[0]
                    route = split_route(route_string)
                    route_data = extract_subpath(path=route, data=data)
                    values[field] = route_data
        return values
