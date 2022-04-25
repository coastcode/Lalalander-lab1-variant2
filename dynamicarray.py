import numpy as np
import ctypes


class Muliter():
    def __init__(self, lis):
        self.data = lis
        self.offset = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.offset >= len(self.data):
            raise StopIteration
        else:
            item = self.data[self.offset]
            self.offset += 1
            return item


class DynamicArray(object):
    def __init__(self):
        self.index = 0
        self.n = 0  # the number of elements now
        self.capacity = 1  # how many elements it can contain
        self.A = self._make_array(self.capacity)  # a low level array

    def is_empty(self):
        """
        :return: true if array is empty, otherwise false
        """
        return self.n == 0

    def __len__(self):
        """
        Gets the length of the current array
        """
        return self.n

    def __getitem__(self, idx):
        """
        Gets the element at idx
        """
        if not 0 <= idx < self.n:  # idx is the array boundary
            raise ValueError("invalid index")
        return self.A[idx]

    def _resize(self, c):
        """
        Resize the capacity of array
        :param c: specific value of capacity
        """
        B = self._make_array(c)  # a new bigger array
        for k in range(self.n):  # reference all existing values
            B[k] = self.A[k]
        self.A = B
        self.capacity = c  # reset the capacity

    # 1.Add a new element
    def add(self, elem):
        if self.n == self.capacity:  # no enough room
            self._resize(2 * self.capacity)
        self.A[self.n] = elem  # add elem to the position of n
        self.n += 1

    # 2.Set an element with specific index / key
    def set(self, idx, elem):
        """
        Replace some element at idx with elem.
        """
        if idx < 0 or idx >= self.n:  # idx is in the boundary
            raise ValueError("invalid index")
        self.A[idx] = elem

    # 3.Remove an element
    def remove_by_index(self, idx):
        """
        Removes the element at the specified index position
        :param idx: specified index
        """
        if idx >= self.n or idx < 0:
            raise ValueError("invalid index")
        for i in range(idx, self.n - 1):
            self.A[i] = self.A[i + 1]
        self.A[self.n - 1] = None
        self.n -= 1

    def remove_by_value(self, value):
        for k in range(self.n):
            if self.A[k] == value:
                for j in range(k, self.n - 1):
                    self.A[j] = self.A[j + 1]
                self.A[self.n - 1] = None
                self.n -= 1
                return
        raise ValueError("value not found")

    # 4.Access
    def size(self):
        """
        Get the size of array
        :return: the value of size
        """
        return self.__len__()

    def member(self, elem):
        """
        Check whether the given element is a member of the array
        :param elem: specified value
        :return:
        """
        for k in range(self.n):
            if self.A[k] == elem:
                return True
        return False

    def reverse(self):
        B = self._make_array(self.capacity)
        for k in range(self.n):
            B[k] = self.A[self.n - 1 - k]
        self.A = B

    # 5.Conversion from/to built-in list
    def convert_to_list(self):
        """
        Convert an array to a list
        :return: converted list
        """
        list_A = []
        for i in range(self.__len__()):
            list_A.append(self.A[i])
        return list_A

    def convert_from_list(self, list_variable):
        c = len(list_variable)
        if c==0:
            c = 1
        B = self._make_array(c)
        for k in range(len(list_variable)):
            B[k] = list_variable[k]
        self.capacity = c
        self.A = B
        self.n = len(list_variable)
        return self

    # 6.Filter data structure by specific predicate
    def filter(self, predicate):
        i = 0
        while i < self.n:
            if not predicate(self.A[i]):
                self.remove_by_index(i)
            else:
                i += 1

    # 7.Map structure by specific function
    def map(self, func):
        """
        Apply the func into the object
        :param func: specific function
        :return: result that applied function
        """
        size = self.__len__()
        if size != 0:
            for i in range(size):
                self.A[i] = func(self.A[i])

    # 8.process elements to build a return value by specific functions
    def reduce(self, func, initial=None):
        """
        Process elements by a specific function
        :param func: specified function
        :param initial: initial state
        :return: the result of processed
        """
        if initial is None:
            return self.A[0]
        else:
            value = initial
        size = self.__len__()
        if size != 0:
            for i in range(size):
                value = func(value, self.A[i])
        return value

    # 9.Iterator
    def __iter__(self):
        return Muliter(self)

    def __next__(self):
        i = self.index
        if i < self.n:
            self.index = i + 1
            return self.A[i]
        else:
            raise StopIteration

    # 10.empty and concat
    def empty(self):
        self.n = 0
        return self

    def concat(self,dy):
        for k in range(dy.n):
            self.add(dy[k])
        return self

    @staticmethod
    def _make_array(c):
        """
        Create a new array of capacity c
        :param c: the capacity of array
        :return: return new array
        """
        return (c * ctypes.py_object)()

    def insert(self, k, value):
        """
        Insert a new element into array at position k
        :param k: insertion position
        :param value: new element
        """
        if self.n == self.capacity:  # no enough room
            self._resize(2 * self.capacity)
        for j in range(self.n, k, -1):
            self.A[j] = self.A[j - 1]
        self.A[k] = value
        self.n += 1

    def _print(self):
        for i in range(self.n):
            print(self.A[i], end=' ')
        print()
