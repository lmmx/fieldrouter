from fieldrouter.generic import R, Route, Routed, Router

__all__ = ("Where", "What")


class Where(Router):
    field_1: Route = "a.aa.aaa.0"
    field_2: Route = "a.aa.aaa.1"
    field_3: Route = "b.bb.2"


class What(Routed[R], extra="forbid"):
    field_1: str
    field_2: str
    field_3: int


json_str = '{"a":{"aa":{"aaa":["value_1","value_2"]}},"b":{"bb":[3,4,5]}}'
result = What[Where].model_validate_json(json_str)

result_dict = result.model_dump()
print(result_dict)

assert result_dict == {"field_1": "value_1", "field_2": "value_2", "field_3": 5}
