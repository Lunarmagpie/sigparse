# sigparse

Backports python3.10 typing features into python 3.7, 3.8, and 3.9.

## Example

```python
import sigparse

def func(param_a: list[str], param_b: str | int, param_c: tuple[int | None]):
    ...

# This returns the same result in python 3.7, 3.8, 3.9, and 3.10!
sigparse.sigparse(func)
```

### PEP604
By default PEP 604 (| for unions) is only enabled for `sigparse.sigparse`.
To enable globally:
```python
import sigparse
sigparse.global_PEP604()
```

## Notes
### Inspect

This module uses inspect behind the scenes. For that reason:

- `sigparse.Parameter.default` is `inspect._empty` when there is no default value.
- `sigparse.Parameter.kind` is `inspect._ParameterKind`.


### Annotated
`typing.Annotated` will always be evaluated with `include_extras=True` in python3.9.
