import types
import typing

__all__: typing.Sequence[str] = ("unwrap",)

try:
    UnionType = types.UnionType  # type: ignore
except AttributeError:
    UnionType = ...

NoneType = type(None)


def _get_origin(typehint: typing.Any) -> typing.Any:
    if hasattr(typehint, "__origin__"):
        return typehint.__origin__

    return None


def _get_args(typehint: typing.Any) -> typing.Any:
    if hasattr(typehint, "__args__"):
        return typehint.__args__

    return None


def unwrap(typehint: typing.Any) -> typing.Any:
    """
    Remove the `None` values from a `Union[T, U]` or `Optional[T]`.

    If one of `T` or `U` is `None`, return the non-none value.
    If `T` and `U` are `None`, return `None`.
    If neither `T` or `U` are `None`, return `Union[T, U]`.
    If `typehint` is not a `Union` or `Option` return `typehint`.
    """

    if typehint is NoneType:
        return None

    if _get_origin(typehint) not in {typing.Union, UnionType}:
        return typehint

    args = _get_args(typehint)

    if not args:
        return None

    hints = list(filter(lambda x: x not in {NoneType, None}, args))

    if len(hints) == 1:
        return hints[0]

    return typing.Union[hints[0], hints[1]]
