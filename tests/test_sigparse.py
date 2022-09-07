from __future__ import annotations

import inspect
import sigparse
import typing


def test_union():
    def func(param: int | str):
        ...

    param = next(iter(sigparse.sigparse(func)))

    assert param.name == "param"
    assert param.annotation == typing.Union[int | str]
    assert param.default == inspect._empty
    assert param.kind == inspect._ParameterKind.POSITIONAL_OR_KEYWORD


def test_subscriptable():
    def func(
        _dict: dict[typing.Any],
        _list: list[typing.Any],
        _tuple: tuple[typing.Any],
        _type: type[typing.Any],
    ):
        ...

    # Subscripting worked properly if this passed without errors.
    sigparse.sigparse(func)
