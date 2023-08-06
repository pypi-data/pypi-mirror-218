# like functools.reduce but with exception handling, args and kwargs

## pip install reduceplus 

## Example Usage

The function reduce_plus takes a function parameter, which should be a callable 
object that accepts two arguments and performs a reduction operation.
 The sequence parameter is an iterable sequence of elements that will be reduced. 
 The optional initial parameter provides an initial value for the reduction. 
 If no initial value is provided and the sequence is empty, a TypeError is raised.

The args and kwargs parameters allow for additional positional and keyword arguments 
to be passed to the function. The ignore_exceptions parameter determines whether exceptions 
raised during the reduction process are ignored (True) or propagated (False). 
By default, exceptions are ignored.

The function iterates over the sequence, using the initial value or the first 
element as the starting point. For each element, the function is called with the 
current value, the element, and any additional arguments and keyword arguments. 
If an exception is raised during the reduction process and ignore_exceptions is 
False, the exception is propagated, terminating the reduction.

Finally, the function returns the final reduced value.

```python
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
```