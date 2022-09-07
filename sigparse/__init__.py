from __future__ import annotations

import dataclasses
import typing
import sys
import inspect
import forbiddenfruit  # type: ignore


__all__: typing.Sequence[str] = ("sigparse", "Parameter")


def _PEP604() -> None:
    """
    Allow writing union types as X | Y
    """

    def _union_or(left: typing.Any, right: typing.Any) -> typing.Any:
        return typing.Union[left, right]

    setattr(typing._GenericAlias, "__or__", _union_or)  # type: ignore
    setattr(typing._GenericAlias, "__ror__", _union_or)  # type: ignore

    forbiddenfruit.curse(type, "__or__", _union_or)


if sys.version_info < (3, 10):
    _PEP604()


@dataclasses.dataclass
class Parameter:
    """
    `default` is `inspect._empty` when there is no default.
    """
    name: str
    annotation: typing.Any
    default: typing.Any
    kind: inspect._ParameterKind


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


def sigparse(func: typing.Callable[..., typing.Any]) -> typing.Sequence[Parameter]:
    if sys.version_info >= (3, 10):
        return inspect.signature(func, eval_str=True).parameters.values()

    localns: dict[str, typing.Any] = {
        "list": typing.List,
        "type": typing.Type,
        "dict": typing.Dict,
        "tuple": typing.Tuple,
    }

    if sys.version_info >= (3, 9):
        type_hints: dict[str, typing.Any] = typing.get_type_hints(
            func, include_extras=True, localns=localns
        )
    else:
        type_hints = typing.get_type_hints(func, localns=localns)

    sig = inspect.signature(func)

    return [_convert_signiture(param, type_hints) for param in sig.parameters.values()]
