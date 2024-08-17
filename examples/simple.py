from fieldrouter import Routing, RoutingModel


class DataRouter(RoutingModel):
    some_value: Routing(int, via="path.to.the.value.0")


data = {"path": {"to": {"the": {"value": [100]}}}}
result = DataRouter.model_validate(data)

print(result.model_dump())  # {'some_value': 100}

assert result.some_value == 100
assert result.model_dump() == {"some_value": 100}
