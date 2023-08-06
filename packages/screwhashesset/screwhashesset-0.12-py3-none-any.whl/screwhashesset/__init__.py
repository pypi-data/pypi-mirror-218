from collections.abc import Set
from collections import deque
from copy import deepcopy, copy
from functools import reduce


class ScrewHashesSet(Set):
    """A custom set implementation that preserves element order and allows efficient element addition and removal.
    Inherits from the abstract base class 'Set'."""

    def __init__(self, i, /):
        """
        Initialize the ScrewHashesSet with an iterable.

        Args:
            i (Iterable): An iterable of elements to initialize the set with.
        """
        self.elements = deque([])
        [self.elements.append(_) for _ in i if _ not in self.elements]

    def __str__(self):
        """
        Get the string representation of the ScrewHashesSet.

        Returns:
            str: The string representation of the ScrewHashesSet.
        """
        return "{" + str(self.elements)[7:-2] + "}"

    def __repr__(self):
        """
        Get the string representation of the ScrewHashesSet.

        Returns:
            str: The string representation of the ScrewHashesSet.
        """
        return f"ScrewHashesSet({repr(self.elements)[6:-1]})"

    def __iter__(self):
        """
        Return an iterator over the elements of the ScrewHashesSet.

        Returns:
            Iterator: An iterator over the elements of the ScrewHashesSet.
        """
        return iter(self.elements)

    def __contains__(self, value):
        """
        Check if a value is present in the ScrewHashesSet.

        Args:
            value: The value to check for containment.

        Returns:
            bool: True if the value is present, False otherwise.
        """
        return value in self.elements

    def __len__(self):
        """
        Get the number of elements in the ScrewHashesSet.

        Returns:
            int: The number of elements in the ScrewHashesSet.
        """
        return len(self.elements)

    def __add__(self, other, /):
        """
        Return a new ScrewHashesSet that is the union of this set and another set or iterable.

        Args:
            other (Set or Iterable): The set or iterable to perform the union with.

        Returns:
            ScrewHashesSet: A new ScrewHashesSet that is the union of this set and the other set or iterable.
        """
        tmpelements = deque([])
        for o in other:
            if not self._isin(o):
                tmpelements.append(o)
        return self.__class__(tmpelements + self.elements.copy())

    def _isin(self, o):
        """
        Check if an element is present in the ScrewHashesSet.

        Args:
            o: The element to check for presence.

        Returns:
            bool: True if the element is present, False otherwise.
        """
        if o in self.elements:
            return True
        return False

    def add(self, other, /):
        """
        Add an element to the ScrewHashesSet.

        Args:
            other: The element to add.
        """
        if not self._isin(other):
            self.elements.append(other)

    def clear(self):
        """
        Remove all elements from the ScrewHashesSet.
        """
        self.elements.clear()

    def copy(self):
        """
        Create a shallow copy of the ScrewHashesSet.

        Returns:
            ScrewHashesSet: A shallow copy of the ScrewHashesSet.
        """
        try:
            return self.__class__(deepcopy(self.elements))
        except Exception:
            return self.__class__(copy(self.elements))

    def _convert_all_iters(self, *others):
        """
        Convert all input arguments to instances of ScrewHashesSet if they are not already one.

        Args:
            *others: Variable number of input arguments to convert.

        Returns:
            deque: A deque containing all the converted ScrewHashesSet instances.
        """
        allothers = deque([])
        for other in others:
            if not isinstance(other, self.__class__):
                other = self.__class__(other)
            allothers.append(other)
        return allothers

    def difference(self, *others):
        """
        Return a new ScrewHashesSet with elements that are in the current set but not in any of the other sets.

        Args:
            *others: Variable number of sets to compute the difference with.

        Returns:
            ScrewHashesSet: A new ScrewHashesSet containing the elements that are in the current set but not in any of the other sets.
        """
        allothers = self._convert_all_iters(*others)
        return reduce(lambda a, b: a - b, allothers, self)

    def intersection(self, *others):
        """
        Return a new ScrewHashesSet with elements that are common to the current set and all the other sets.

        Args:
            *others: Variable number of sets to compute the intersection with.

        Returns:
            ScrewHashesSet: A new ScrewHashesSet containing the elements that are common to the current set and all the other sets.
        """
        allothers = self._convert_all_iters(*others)
        return reduce(lambda a, b: a & b, allothers, self)

    def intersection_update(self, *others):
        """
        Update the current ScrewHashesSet with elements that are common to the current set and all the other sets.

        Args:
            *others: Variable number of sets to compute the intersection with.
        """
        elements = self.intersection(*others).copy()
        self.elements = elements.elements

    def difference_update(self, *others):
        """
        Update the current ScrewHashesSet with elements that are in the current set but not in any of the other sets.

        Args:
            *others: Variable number of sets to compute the difference with.
        """
        elements = self.difference(*others).copy()
        self.elements = elements.elements

    def discard(self, elem, /):
        """
        Remove an element from the set if it is present.

        Args:
            elem: The element to be removed from the set.
        """
        if self._isin(elem):
            self.elements.remove(elem)

    def isdisjoint(self, other, /):
        """
        Check if the current set has no elements in common with the other set.

        Args:
            other: The set to compare with.

        Returns:
            bool: True if the sets are disjoint (have no elements in common), False otherwise.
        """
        return not self.intersection(other)

    def issubset(self, other, /):
        """
        Check if every element in the current set is also in the other set.

        Args:
            other: The set to compare with.

        Returns:
            bool: True if every element in the current set is also in the other set, False otherwise.
        """
        return self <= other

    def issuperset(self, other, /):
        """
        Check if every element in the other set is also in the current set.

        Args:
            other: The set to compare with.

        Returns:
            bool: True if every element in the other set is also in the current set, False otherwise.
        """
        return self >= other

    def pop(self):
        """
        Remove and return the rightmost element from the ScrewHashesSet.

        Returns:
            object: The removed element.

        Raises:
            KeyError: If the ScrewHashesSet is empty.
        """
        return self.elements.pop()

    def remove(self, elem, /):
        """
        Remove the specified element from the ScrewHashesSet.

        Args:
            elem: The element to remove.

        Raises:
            KeyError: If the element is not present in the ScrewHashesSet.
        """
        self.elements.remove(elem)

    def symmetric_difference(self, *others):
        """
        Compute the symmetric difference between the ScrewHashesSet and multiple other sets.

        Args:
            *others: Variable length argument list of other sets.

        Returns:
            ScrewHashesSet: A new ScrewHashesSet containing elements that are present in exactly one of the sets.
        """
        allothers = self._convert_all_iters(*others)
        return reduce(lambda a, b: a ^ b, allothers, self)

    def symmetric_difference_update(self, *others):
        """
        Update the ScrewHashesSet with the symmetric difference between itself and multiple other sets.

        Args:
            *others: Variable length argument list of other sets.
        """
        elements = self.symmetric_difference(*others).copy()
        self.elements = elements.elements

    def union(self, *others):
        """
        Compute the union of the ScrewHashesSet and multiple other sets.

        Args:
            *others: Variable length argument list of other sets.

        Returns:
            ScrewHashesSet: A new ScrewHashesSet containing all unique elements from all sets.
        """
        allothers = self._convert_all_iters(*others)
        return reduce(lambda a, b: a | b, allothers, self)

    def update(self, *others):
        """
        Update the ScrewHashesSet by adding elements from multiple other sets.

        Args:
            *others: Variable length argument list of other sets.
        """
        elements = self.union(*others).copy()
        self.elements = elements.elements

    def append(self, other, /):
        """
        Append an element to the ScrewHashesSet.

        Args:
            other: The element to append.
        """
        self.add(other)

    def appendleft(self, elem, /):
        """
        Append an element to the beginning of the ScrewHashesSet if it is not already present.

        Args:
            elem: The element to append.
        """
        if not self._isin(elem):
            self.elements.appendleft(elem)

    def extend(self, elem, /):
        """
        Extend the ScrewHashesSet by adding elements from an iterable.

        Args:
            elem: An iterable containing elements to add to the ScrewHashesSet.
        """
        for e in elem:
            self.add(e)

    def extendleft(self, elem, /):
        """
        Extend the ScrewHashesSet by adding elements from an iterable to the beginning, if they are not already present.

        Args:
            elem: An iterable containing elements to add to the ScrewHashesSet.
        """
        for e in elem:
            if not self._isin(elem):
                self.elements.appendleft(e)

    def index(self, x, start=None, stop=None, /):
        """
        Return the index of the first occurrence of an element in the ScrewHashesSet.

        Args:
            x: The element to search for.
            start (optional): The starting index for the search. If not provided, the search starts from index 0.
            stop (optional): The stopping index for the search. If not provided, the search stops at the last index.

        Returns:
            int: The index of the first occurrence of the element in the ScrewHashesSet.

        Raises:
            ValueError: If the element is not found in the ScrewHashesSet.
        """
        if not start:
            start = 0
        if not stop:
            stop = len(self.elements) - 1
        return self.elements.index(x, start, stop)

    def popleft(self):
        """
        Remove and return the leftmost element from the ScrewHashesSet.

        Returns:
            The leftmost element from the ScrewHashesSet.

        Raises:
            IndexError: If the ScrewHashesSet is empty.
        """
        return self.elements.popleft()

    def reverse(self):
        """
        Reverse the order of elements in the ScrewHashesSet.
        """
        self.elements.reverse()

    def rotate(self, n=1, /):
        """
        Rotate the elements in the ScrewHashesSet by a specified number of steps.

        Args:
            n (optional): The number of steps to rotate the elements. Positive values rotate to the right,
                          and negative values rotate to the left. The default is 1.
        """
        self.elements.rotate(n)

    def insert(self, i, x, /):
        """
        Insert an element at a specified index in the ScrewHashesSet.

        Args:
            i: The index at which to insert the element.
            x: The element to insert.
        """
        if not self._isin(x):
            self.elements.insert(i, x)


