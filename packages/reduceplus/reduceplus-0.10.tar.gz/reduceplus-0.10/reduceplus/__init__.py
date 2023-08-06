_initial_missing = object()


def reduce_plus(
    function,
    sequence,
    initial=_initial_missing,
    /,
    args=(),
    kwargs=None,
    ignore_exceptions=True,
):
    """
    Perform a reduction operation on a sequence using the specified function.

    Args:
        function: A callable object that takes two arguments and performs
            a reduction operation.
        sequence: An iterable sequence of elements to be reduced.
        initial (optional): An initial value for the reduction. If not provided,
            the first element of the sequence is used as the initial value.
        / (slash): Separates positional-only arguments from positional or keyword arguments.
        args (optional): Additional positional arguments to be passed to the function.
        kwargs (optional): Additional keyword arguments to be passed to the function.
        ignore_exceptions (optional): If True, exceptions raised during the reduction
            process will be ignored and the reduction will continue. If False, the
            exception will be propagated, terminating the reduction. Default is True.

    Returns:
        The final reduced value.

    Raises:
        TypeError: If the sequence is empty and no initial value is provided.

    Examples:
        from reduceplus import reduce_plus
        ba = reduce_plus(
        operator.add, ["dddd", 222, 434, "dddds"], 'xxxx', ignore_exceptions = True)
        print(ba)
        xxxxdddddddds

        ba = reduce_plus(
        operator.add, ["dddd", 222, 434, "dddds"], 20, ignore_exceptions = True)
        print(ba)
        676
    """
    if not kwargs:
        kwargs = {}
    it = iter(sequence)

    if initial is _initial_missing:
        try:
            value = next(it)
        except StopIteration:
            raise TypeError(
                "reduce() of empty iterable with no initial value"
            ) from None
    else:
        value = initial

    for element in it:
        try:
            value = function(value, element, *args, **kwargs)
        except Exception as fe:
            if not ignore_exceptions:
                raise fe

    return value
