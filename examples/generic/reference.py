from fieldrouter.generic import R, Route, Routed, Router
from pydantic import Field


class Where(Router):
    referent: Route = "first.part"
    a: Route = ".referent.a"
    b: Route = ".referent.b.0"
    c: Route = ".referent.c.value.0"


class What(Routed[R]):
    referent: dict = Field(exclude=True)
    a: int
    b: int
    c: int


data = {"first": {"part": {"a": 1, "b": [2], "c": {"value": [3]}}}}
result = What[Where].model_validate(data)

print(result.model_dump())  # {'a': 1, 'b': 2, 'c': 3}

assert result.a == 1
assert result.b == 2
assert result.c == 3
assert result.model_dump() == {"a": 1, "b": 2, "c": 3}
