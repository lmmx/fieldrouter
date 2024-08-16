# fieldrouter: Data model validation for nested data routes

`fieldrouter` is a Python library that provides helpers for modelling routes in highly nested structured data.

It should be considered for cases when exhaustively modelling the tree structures involved is
surplus to requirements (in other cases you would simply use Pydantic in the regular way),
or perhaps if you want to specify 'routes' on an existing data model.

For example to access the number 30 in

```py
data = {"a": {"aa": {"aaa": [10, 20, 30]}}}
```

You would typically need to write Pydantic models for each level

```py
class A(BaseModel):
    a: AA

class AA(BaseModel):
    aa: AAA

class AAA(BaseModel):
    aaa: list[int]

thirty = A.model_validate(data).a.aa.aaa[2]
```

With `fieldrouter` you would instead specify a 'route' for the subpath on a 'router' model
(which is just a regular Pydantic model with default argument validation):

```py
from fieldrouter import RouterModel, Route

class Where(RouterModel):
    thirty: Route = "a.aa.aaa.2"
```

Then you can model the value at that route with a corresponding field on a 'routed' model
(which is a generic model which takes the router as a type argument):

```py
from fieldrouter import Routed, R

class What(Routed[R]):
    thirty: int
```

Then you can use the router class as a generic type argument to the instance of the routee:

```py
model = What[Where].model_validate(data)
```
