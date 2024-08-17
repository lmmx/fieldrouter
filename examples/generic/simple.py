from fieldrouter.generic import R, Route, Routed, Router


class Where(Router):
    some_value: Route = "path.to.the.value.0"


class What(Routed[R]):
    some_value: int


data = {"path": {"to": {"the": {"value": [100]}}}}
result = What[Where].model_validate(data)

print(result.model_dump())  # {'some_value': 100}

assert result.some_value == 100
assert result.model_dump() == {"some_value": 100}
