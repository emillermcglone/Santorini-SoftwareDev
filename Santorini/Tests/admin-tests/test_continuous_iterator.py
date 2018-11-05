import pytest
import sys, os
dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, dir_path + '/../../')

from Lib.continuous_iterator import ContinuousIterator

@pytest.fixture
def items():
    return [1, 2, 3]


@pytest.fixture
def iterator(items):
    return iter(ContinuousIterator(items))


@pytest.fixture
def empty_iterator():
    return iter(ContinuousIterator([]))


def test_empty_list(empty_iterator):
    for i in empty_iterator:
        assert i is not None


def test_iterate_at_least_once(items, iterator):
    for i, j in zip(items, iterator):
        assert i is j


def test_iterator_loop_around(items, iterator):
    items = items * 10
    for i, j in zip(items, iterator):
        assert i is j

