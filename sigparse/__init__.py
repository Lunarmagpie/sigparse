# MIT License

# Copyright (c) 2022 Lunarmagpie
# L37-L51 Copyright (c) 2022 Endercheif

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from __future__ import annotations

import dataclasses
import typing
import sys
import inspect
import forbiddenfruit  # type: ignore


__all__: typing.Sequence[str] = ("sigparse", "Parameter", "global_PEP604")


def _apply_PEP604() -> None:
    """
    Allow writing union types as X | Y
    """

    if sys.version_info >= (3, 10):
        return

    def _union_or(left: typing.Any, right: typing.Any) -> typing.Any:
        return typing.Union[left, right]

    setattr(typing._GenericAlias, "__or__", _union_or)  # type: ignore
    setattr(typing._GenericAlias, "__ror__", _union_or)  # type: ignore

    forbiddenfruit.curse(type, "__or__", _union_or)


def _revert_PEP604() -> None:
    if sys.version_info >= (3, 10):
        return

    forbiddenfruit.reverse(type, "__or__")


GLOBAL_PEP604 = False


def global_PEP604() -> None:
    global GLOBAL_PEP604
    GLOBAL_PEP604 = True
    _apply_PEP604()


@dataclasses.dataclass
class Parameter:
    """
    `default` and `annotation` are `inspect._empty` when there is no default or
    annotation respectively.
    """

    name: str
    annotation: typing.Any
    default: typing.Any
    kind: inspect._ParameterKind

    @property
    def has_default(self) -> bool:
        """
        Return `True` if this argument has a default value.
        """
        return self.default is not inspect._empty

    @property
    def has_annotation(self) -> bool:
        """
        Return `True` if this argument has an annotation.
        """
        return self.annotation is not inspect._empty


def _convert_signiture(
    param: inspect.Parameter, type_hints: dict[str, type[typing.Any]]
) -> Parameter:
    annotation = type_hints.get(param.name)
    return Parameter(
        name=param.name,
        annotation=annotation or param.annotation,
        default=param.default,
        kind=param.kind,
    )


def sigparse(func: typing.Callable[..., typing.Any]) -> list[Parameter]:
    if sys.version_info >= (3, 10):
        return [
            _convert_signiture(param, {})
            for param in inspect.signature(func, eval_str=True).parameters.values()
        ]

    localns: dict[str, typing.Any] = {
        "list": typing.List,
        "type": typing.Type,
        "dict": typing.Dict,
        "tuple": typing.Tuple,
    }

    if not GLOBAL_PEP604:
        _apply_PEP604()

    if sys.version_info >= (3, 9):
        type_hints: dict[str, typing.Any] = typing.get_type_hints(
            func, include_extras=True, localns=localns
        )
    else:
        type_hints = typing.get_type_hints(func, localns=localns)

    sig = inspect.signature(func)

    if not GLOBAL_PEP604:
        _revert_PEP604()

    return [_convert_signiture(param, type_hints) for param in sig.parameters.values()]
