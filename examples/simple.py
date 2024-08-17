from fieldrouter import Routing, RoutingModel


class DataRouter(RoutingModel):
    my_value: Routing(int, "path.to.the.value.0")
    with_via: Routing(int, via="path.to.the.value.0")


data = {"path": {"to": {"the": {"value": [100]}}}}
result = DataRouter.model_validate(data)

print(result.model_dump())  # {'my_value': 100, 'with_via': 100}

assert result.my_value == 100
assert result.with_via == 100
assert result.model_dump() == {"my_value": 100, "with_via": 100}
