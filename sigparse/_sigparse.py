# MIT License

# Copyright (c) 2022 Lunarmagpie

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
import inspect

from sigparse._applicator import Applicator

__all__: typing.Sequence[str] = ("sigparse", "Parameter", "Signature")


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


@dataclasses.dataclass
class Signature:
    parameters: list[Parameter]
    return_annotation: typing.Any


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


class Sigparse(Applicator[typing.Any, Signature]):
    @typing.no_type_check
    def gt_or_eq_310(self, func: typing.Any) -> Signature:
        sig = inspect.signature(func, eval_str=True)
        parameters = [
            _convert_signiture(param, {}) for param in sig.parameters.values()
        ]
        return Signature(parameters=parameters, return_annotation=sig.return_annotation)

    @typing.no_type_check
    def eq_309(self, func: typing.Any) -> Signature:
        sig = inspect.signature(func)
        type_hints = typing.get_type_hints(func, include_extras=True)
        parameters = [
            _convert_signiture(param, type_hints) for param in sig.parameters.values()
        ]
        return Signature(parameters=parameters, return_annotation=sig.return_annotation)

    @typing.no_type_check
    def lt_or_eq_308(self, func: typing.Any, localns: dict[str, type]) -> Signature:
        sig = inspect.signature(func)
        type_hints = typing.get_type_hints(func, localns=localns)
        parameters = [
            _convert_signiture(param, type_hints) for param in sig.parameters.values()
        ]
        return Signature(parameters=parameters, return_annotation=sig.return_annotation)


def sigparse(func: typing.Any) -> Signature:
    return Sigparse(func)()
