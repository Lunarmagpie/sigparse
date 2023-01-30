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
import inspect


import typing

from sigparse._applicator import Applicator


__all__: typing.Sequence[str] = ("classparse", "ClassVar")


@dataclasses.dataclass(frozen=True)
class ClassVar:
    """
    `default` is `inspect._empty` when there is no default value.
    """

    name: str
    annotation: typing.Any
    default: typing.Any

    @property
    def has_default(self) -> bool:
        """
        Return `True` if this class var has a default value.
        """
        return self.default is not inspect._empty


def _convert_parameter(name: str, annotation: typing.Any, cls: typing.Any) -> ClassVar:
    return ClassVar(
        name=name, annotation=annotation, default=cls.__dict__.get(name, inspect._empty)
    )


def convert_result(
    wrap: typing.Callable[..., dict[str, type]]
) -> typing.Callable[..., list[ClassVar]]:
    def inner(
        self: Classparse, cls: type, *args: typing.Any, **kwargs: typing.Any
    ) -> list[ClassVar]:
        return [
            _convert_parameter(name, annotation, cls)
            for name, annotation in wrap(self, cls, *args, **kwargs).items()
        ]

    return inner


class Classparse(Applicator[type, "list[ClassVar]"]):
    @convert_result
    @typing.no_type_check
    def gt_or_eq_310(self, cls: type) -> dict[str, type]:
        return typing.get_type_hints(cls, include_extras=True)

    eq_309 = gt_or_eq_310

    @convert_result
    @typing.no_type_check
    def lt_or_eq_308(self, cls: type, localns: dict[str, type]) -> dict[str, type]:
        return typing.get_type_hints(cls, localns=localns)


def classparse(cls: type) -> list[ClassVar]:
    return Classparse(cls)()
