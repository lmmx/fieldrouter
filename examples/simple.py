from fieldrouter import Routing, RoutingModel


# You can specify the Routing type annotation with or without keyword arguments
class DataRouter(RoutingModel):
    a_value: Routing(int, "path.to.the.value.0")
    with_via: Routing(int, via="path.to.the.value.0")
    with_kws: Routing(tp=int, via="path.to.the.value.0")


data = {"path": {"to": {"the": {"value": [100]}}}}
result = DataRouter.model_validate(data)

print(result.model_dump())  # {'a_value': 100, 'with_via': 100, 'with_kws': 100}

assert result.a_value == 100
assert result.with_via == 100
assert result.with_kws == 100
assert result.model_dump() == {"a_value": 100, "with_via": 100, "with_kws": 100}
