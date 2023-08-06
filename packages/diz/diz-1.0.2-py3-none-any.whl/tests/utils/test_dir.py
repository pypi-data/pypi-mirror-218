import pytest
from diz.utils import dir


def test_is_empty():
    result = dir.is_empty("tests/utils")
    assert result is False
