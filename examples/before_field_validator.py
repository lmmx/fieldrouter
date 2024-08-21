from fieldrouter import Routing, RoutingModel
from pydantic import ByteSize, field_validator


class Dogs(ByteSize):
    byte_sizes = {"k": 10**3, "m": 100**6, "b": 10**9}


class DataRouter(RoutingModel):
    dogs: Routing(Dogs, "the.value.0")

    @field_validator("dogs", mode="before")
    def no_commas(v) -> str:
        return v.replace(",", "")


data = {"the": {"value": ["1,234 K dogs"]}}
result = DataRouter.model_validate(data)

print(result.model_dump())  # {'dogs': 1234000}

assert result.dogs == 1234000
assert result.model_dump() == {"dogs": 1234000}
