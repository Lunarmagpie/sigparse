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
import abc
import typing
import sys

from sigparse._pep604 import PEP604_CTX

LOCALNS: dict[str, typing.Any] = {
    "list": typing.List,
    "type": typing.Type,
    "dict": typing.Dict,
    "tuple": typing.Tuple,
}


IN = typing.TypeVar("IN")
OUT = typing.TypeVar("OUT")


class Applicator(abc.ABC, typing.Generic[IN, OUT]):
    def __init__(self, obj: IN) -> None:
        if sys.version_info >= (3, 10):
            self.return_value = self.gt_or_eq_310(obj)

        elif sys.version_info >= (3, 9):
            with PEP604_CTX():
                self.return_value = self.eq_309(obj)

        else:
            with PEP604_CTX():
                self.return_value = self.lt_or_eq_308(obj, LOCALNS)

    def __call__(self) -> OUT:
        return self.return_value

    @abc.abstractmethod
    def gt_or_eq_310(self, obj: IN) -> OUT:
        ...

    @abc.abstractmethod
    def eq_309(self, obj: IN) -> OUT:
        ...

    @abc.abstractmethod
    def lt_or_eq_308(self, obj: IN, localns: dict[str, type]) -> OUT:
        ...
