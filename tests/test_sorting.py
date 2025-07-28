import pytest

# Bubble sort tests
from python_practice.examples.sorting import sort_bubble


def test_bubble_sort_ascending():
    test_arr = [-1, 5, 0.5, 3, 1, 9]
    assert sort_bubble(test_arr) == sorted(test_arr, reverse=False)


def test_bubble_sort_descending():
    test_arr = [-1, 5, 0.5, 3, 1, 9]
    assert sort_bubble(test_arr, ascending=False) == \
        sorted(test_arr, reverse=True)
