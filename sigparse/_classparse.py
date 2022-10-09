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


import typing

from sigparse._applicator import Applicator


class Classparse(Applicator[type, "dict[str, type]"]):
    @typing.no_type_check
    def gt_or_eq_310(self, func: typing.Any) -> dict[str, type]:
        return typing.get_type_hints(func, include_extras=True)

    @typing.no_type_check
    def eq_309(self, func: typing.Any) -> dict[str, type]:
        return typing.get_type_hints(func, include_extras=True)

    @typing.no_type_check
    def lt_or_eq_308(
        self, func: typing.Any, localns: dict[str, type]
    ) -> dict[str, type]:
        return typing.get_type_hints(func, localns=localns)


def classparse(cls: type) -> dict[str, type]:
    return Classparse(cls)()
