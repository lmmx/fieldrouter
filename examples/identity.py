"""A route of just a . on its own is the identity (the entire input)."""
from fieldrouter import Routing, RoutingModel


class ModelWithIdentityRef(RoutingModel):
    full: Routing(dict, ".")
    a_normal: Routing(int, "a")
    a_by_ref: Routing(int, ".full.a")  # Note: don't actually do this, it's just to demo!


data = {"a": 1, "b": 2}
result = ModelWithIdentityRef.model_validate(data)

print(result.model_dump())  # {'full': {'a': 1, 'b': 2}, 'a_normal': 1, 'a_by_ref': 1}

assert result.full == {"a": 1, "b": 2}
assert result.a_normal == 1
assert result.a_by_ref == 1
assert result.model_dump() == {"full": {"a": 1, "b": 2}, "a_normal": 1, "a_by_ref": 1}
