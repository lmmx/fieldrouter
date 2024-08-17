"""A route of just a . on its own is the identity (the entire input)."""

from fieldrouter.generic import R, Route, Routed, Router


class Where(Router):
    full: Route = "."
    a_normal: Route = "a"
    a_by_ref: Route = ".full.a"  # Note: don't actually do this, it's just to demo!


class What(Routed[R]):
    full: dict
    a_normal: int
    a_by_ref: int


data = {"a": 1, "b": 2}
result = What[Where].model_validate(data)

print(result.model_dump())  # {'full': {'a': 1, 'b': 2}, 'a_normal': 1, 'a_by_ref': 1}

assert result.full == {"a": 1, "b": 2}
assert result.a_normal == 1
assert result.a_by_ref == 1
assert result.model_dump() == {"full": {"a": 1, "b": 2}, "a_normal": 1, "a_by_ref": 1}
