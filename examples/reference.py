from fieldrouter import Routing, RoutingModel
from pydantic import Field


class ModelWithReferences(RoutingModel):
    referent: Routing(dict, "first.part") = Field(exclude=True)
    a: Routing(int, ".referent.a")
    b: Routing(int, ".referent.b.0")
    c: Routing(int, ".referent.c.value.0")


data = {"first": {"part": {"a": 1, "b": [2], "c": {"value": [3]}}}}
result = ModelWithReferences.model_validate(data)

print(result.model_dump())  # {'a': 1, 'b': 2, 'c': 3}

assert result.a == 1
assert result.b == 2
assert result.c == 3
assert result.model_dump() == {"a": 1, "b": 2, "c": 3}
