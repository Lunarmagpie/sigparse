import typing
import sigparse

def test_unwrap():
    assert sigparse.utils.unwrap(typing.Union[int, None]) == int
    assert sigparse.utils.unwrap(typing.Union[None, None]) == None
    assert sigparse.utils.unwrap(typing.Union[int, str]) == typing.Union[int, str]

    assert sigparse.utils.unwrap(typing.Optional[int]) == int
    assert sigparse.utils.unwrap(typing.Optional[None]) == None

    assert sigparse.utils.unwrap(int) == int
    assert sigparse.utils.unwrap(None) == None
