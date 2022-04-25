import unittest
from hypothesis import given
import hypothesis.strategies as st
import numpy as np
from dynamicarray import DynamicArray


class TestDynamicArray(unittest.TestCase):

    def test_singleton(self):
        d = DynamicArray()
        d.add(55)
        d = d.convert_to_list()
        self.assertEqual(d, [55])

    def test_add(self):
        d = DynamicArray()
        d.add(55)
        d.add(15)
        d = d.convert_to_list()
        self.assertEqual(d, [55, 15])

    def test_set(self):
        d = DynamicArray()
        d.add(55)
        d.add(15)
        d.set(1, 2)
        d = d.convert_to_list()
        self.assertEqual(d, [55, 2])

    def test_remove_by_index(self):
        d = DynamicArray()
        d.add(55)
        d.add(15)
        d.remove_by_index(0)
        d = d.convert_to_list()
        self.assertEqual(d, [15])

    def test_remove_by_value(self):
        d = DynamicArray()
        d.add(55)
        d.add(15)
        d.remove_by_value(55)
        d = d.convert_to_list()
        self.assertEqual(d, [15])

    def test_resize(self):
        d = DynamicArray()
        d._resize(5)
        self.assertEqual(d.capacity, 5)

    def test_size(self):
        d = DynamicArray()
        d.add(55)
        d.add(15)
        self.assertEqual(d.size(), 2)

    def test_is_empty(self):
        d = DynamicArray()
        d.add(55)
        d.add(15)
        d.empty()
        self.assertEqual(d.is_empty(), True)

    def test_member(self):
        d = DynamicArray()
        d.add(55)
        d.add(15)
        self.assertEqual(d.member(15), True)

    def test_reverse(self):
        d = DynamicArray()
        d.add(55)
        d.add(15)
        d.add(2)
        d.add(8)
        d.reverse()
        d = d.convert_to_list()
        self.assertEqual(d, [8, 2, 15, 55])

    def test_convert_from_list(self):
        d = DynamicArray().convert_from_list([1, 1, 33])
        d.add(2)
        d = d.convert_to_list()
        self.assertEqual(d, [1, 1, 33, 2])

    def test_filter(self):
        d = DynamicArray().convert_from_list([1, 12, 3, 98, 5])
        d.filter(lambda x: x % 2 != 0)
        d = d.convert_to_list()
        self.assertEqual(d, [1, 3, 5])

    def test_map(self):
        d = DynamicArray().convert_from_list([1, 12, 3])
        d.map(lambda x: x + 1)
        d = d.convert_to_list()
        self.assertEqual(d, [2, 13, 4])

    def test_reduce(self):
        # sum of empty list
        demp = DynamicArray()
        self.assertEqual(demp.reduce(lambda x, y: x + y, 0), 0)

        # sum of list
        d = DynamicArray().convert_from_list([1, 12, 3])
        v = d.reduce(lambda x, y: x + y, 0)
        self.assertEqual(v, 16)

    @given(st.lists(st.integers()))
    def test_from_list_to_list_equality(self, a):
        d = DynamicArray()
        d.convert_from_list(a)
        b = d.convert_to_list()
        self.assertEqual(a, b)

    @given(st.lists(st.integers()))
    def test_python_len_and_list_size_equality(self, a):
        # This will generate lists of arbitrary length
        # usually 0~100 elements whose elements are integers.
        d = DynamicArray()
        d.convert_from_list(a)
        self.assertEqual(d.size(), len(a))

    @given(st.lists(st.integers()))
    def test_monoid_concat_empty(self, a):
        d = DynamicArray()
        d.convert_from_list(a)
        d1 = DynamicArray()
        d1.convert_from_list(a)
        e = DynamicArray()
        d.concat(e)
        b = d.convert_to_list()
        c = d1.convert_to_list()
        self.assertEqual(b, c)

    @given(
        a=st.lists(st.integers()),
        b=st.lists(st.integers()),
        c=st.lists(st.integers()))
    def test_monoid_concat(self, a, b, c):
        d1 = DynamicArray()
        d1.convert_from_list(a)
        d2 = DynamicArray()
        d2.convert_from_list(b)
        d3 = DynamicArray()
        d3.convert_from_list(c)
        d12 = DynamicArray()
        d12.convert_from_list(a)
        d1.concat(d2)
        d1.concat(d3)
        d2.concat(d3)
        d12.concat(d2)
        b = d1.convert_to_list()
        c = d12.convert_to_list()
        self.assertEqual(b, c)

    def test_iter(self):
        x = [1, 2, 3]
        d = DynamicArray()
        d.convert_from_list(x)
        tmp = []
        for e in d:
            tmp.append(e)
        self.assertEqual(x, tmp)
        self.assertEqual(d.convert_to_list(), tmp)

        i = iter(DynamicArray())
        self.assertRaises(StopIteration, lambda: next(i))
