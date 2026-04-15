from pytest import raises

from fieldrouter import Routing, RoutingModel


def test_bad_route():
    # Route miss due to incorrect type: leaf is a list not a dict
    class DataRouter(RoutingModel):
        a_value: Routing(int, "path.to.the.value.MISTYPE_MISS")

    data = {"path": {"to": {"the": {"value": [100]}}}}
    with raises(TypeError, match="No dict"):
        DataRouter.model_validate(data)
