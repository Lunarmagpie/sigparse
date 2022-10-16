import typing

def unwrap(typehint: typing.Any) -> typing.Any:
    """
    Remove the `None` values from a `Union[T, U]` or `Optional[T]`.

    If one of `T` or `U` is `None`, return the non-none value.
    If `T` and `U` are `None`, return `None`.
    If neither `T` or `U` are `None`, return `Union[T, U]`.
    """

    args = typing.get_args(typehint)

    if not args:
        return None

    hints = list(filter(lambda x: x is not None, args))

    if len(hints) == 1:
        return hints[0]

    return typing.Union[hints[0], hints[1]]
