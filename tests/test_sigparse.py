from __future__ import annotations

import inspect
import sys
import sigparse
import typing
import pytest


def test_union():
    def func(param: int | str):
        ...

    param = next(iter(sigparse.sigparse(func)))

    assert param.name == "param"
    assert param.annotation == typing.Union[typing.Union[int, str]]
    assert param.default == inspect._empty
    assert param.kind == inspect._ParameterKind.POSITIONAL_OR_KEYWORD


def test_subscriptable():
    def func(
        _dict: dict[typing.Any, typing.Any],
        _list: list[typing.Any],
        _tuple: tuple[typing.Any],
        _type: type[typing.Any],
    ):
        ...

    # Subscripting worked properly if this passed without errors.
    sigparse.sigparse(func)


@pytest.mark.skipif(sys.version_info >= (3, 10), reason="Feature will always work in this version.")
def test_global_PEP604_disabled():
    with pytest.raises(TypeError):
        int | str


@pytest.mark.skipif(sys.version_info >= (3, 10), reason="Feature will always work in this version.")
def test_global_PEP604_enabled():
    sigparse.global_PEP604()
    int | str
