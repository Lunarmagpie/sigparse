# MIT License

# Copyright (c) 2022 Endercheif

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


import typing
import sys

if sys.version_info < (3, 10):
    import forbiddenfruit  # type: ignore


__all__: typing.Sequence[str] = ("PEP604_CTX",)


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


class PEP604_CTX:
    def __enter__(self) -> None:
        _apply_PEP604()

    def __exit__(self, *_: typing.Any) -> None:
        if not GLOBAL_PEP604:
            _revert_PEP604()
