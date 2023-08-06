# A set that handles all kinds of objects (hashable or not) and preserves the order of the elements

## pip install screwhashesset

#### Tested against Windows 10 / Python 3.10 / Anaconda 


The module implements a data structure called "ScrewHashesSet" 
which is a custom set implementation in Python. 
The ScrewHashesSet combines the functionality of a set and a deque 
(double-ended queue) by using a deque to store the elements and a set 
to efficiently perform membership checks.

The ScrewHashesSet provides various methods to manipulate and interact with the set, 
including adding elements, removing elements, checking for membership, 
performing set operations (e.g., union, intersection, difference), and modifying the set in-place.

This module can be useful for developers who need to work with sets and 
require efficient operations for adding, removing, 
and checking membership of elements, while also having the flexibility of 
a deque for efficient element insertion and removal at both ends of the set. 
The ScrewHashesSet can be particularly beneficial in scenarios 
where the order of elements is important, such as maintaining a 
sorted collection or implementing a queue-like data structure.

### Advantages of using ScrewHashesSet:

#### Efficient Membership Checks: 

The underlying set data structure allows for fast membership checks,
providing constant-time complexity O(1) for determining whether an element is in the set.


#### Flexible Element Manipulation: 

The ScrewHashesSet supports various methods for adding, removing, and modifying elements, 
including insertion at specific indices and removing elements from both ends of the set.

#### Compatibility with Mutable Elements:

An advantage of using the ScrewHashesSet module is its compatibility with mutable elements. 
Unlike the built-in set in Python, which only allows immutable objects as elements, 
the ScrewHashesSet module can handle both mutable and immutable objects.

This means that you can use the ScrewHashesSet to store and manipulate objects that can be modified 
after being added to the set. This flexibility is particularly useful when dealing with 
complex data structures or objects that need to be updated or modified while still being part of the set.

By supporting mutable elements, the ScrewHashesSet module provides developers with the ability 
to work with a wider range of data types and structures, allowing for more flexible and dynamic use cases. 
This advantage enhances the practicality and versatility of the module, making 
it suitable for scenarios where mutable objects need to be stored, manipulated, 
and tracked within a set-like data structure.

#### Preserves Element Order:

The ScrewHashesSet utilizes a deque to maintain the order of elements, 
ensuring that the elements are stored and retrieved in the same order they were added.

#### Set Operations: 

The module includes methods for performing common set operations, such as union, 
intersection, difference, and symmetric difference, allowing developers to combine and 
manipulate sets efficiently.

#### Modifiable In-Place:

Many methods of ScrewHashesSet modify the set in-place, providing the advantage of not requiring 
additional memory allocation when modifying the set's contents.




## Import it 

```python
from screwhashesset import ScrewHashesSet as se
```

## Examples with unmutables

```python
l1 = [
    9,
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    9,
]
l2 = [12, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13]
l3 = [5, 3, 4, 5]
l4 = [19, 20, 21, 22]
s1 = se(l1)
print(f"{s1=}")
print(f"{len(s1)=}")
print(f"{9 in s1=}")
print(f"{19 in s1=}")
print(f"{9 not in s1=}")
print(f"{19 not in s1=}")
print(f"{s1.isdisjoint(se(l4))=}")
print(f"{s1.isdisjoint(l4)=}")
print(f"{s1.issubset(se(l3))=}")
print(f"{s1 <= se(l3)=}")
print(f"{s1 < se(l3)=}")
print(f"{se(l3).issubset(s1)=}")
print(f"{se(l3) <= s1=}")
print(f"{se(l3) < s1=}")

print(f"{s1.issuperset(se(l3))=}")
print(f"{s1 >=se(l3)=}")
print(f"{s1 >se(l3)=}")

print(f"{se(l3).issuperset(s1)=}")
print(f"{se(l3) >= s1=}")
print(f"{se(l3) > s1=}")


print(f"{s1.union(l1,l2,l3,l4)=}")
print(f"{s1.union(se(l1),se(l2),se(l3),se(l4))=}")
print(f"{s1 | l2 | l3 | l4=}")
print(f"{s1 | tuple(l2) | se(l3) | se(l4)=}")

print(f"{[x**2 for x in s1]=}")


print(f"{s1.intersection(l1,l2,l3)=}")
print(f"{s1.intersection(se(l1),se(l2),se(l3))=}")
print(f"{s1 & l2 & l3=}")
print(f"{s1 & tuple(l2) & se(l3)=}")


print(f"{s1.difference(l2,l3)=}")
print(f"{s1.difference(se(l2),se(l3))=}")
print(f"{s1 - l2 - l3=}")
print(f"{s1 - tuple(l2) - se(l3)=}")

print(f"{s1.symmetric_difference(l2,l3)=}")
print(f"{s1.symmetric_difference(se(l2),se(l3))=}")
print(f"{s1 ^ l2 ^ l3=}")
print(f"{s1 ^ tuple(l2) ^ se(l3)=}")

s6 = s1.copy()
print(f"{s6 is s1=}")
print(f"{s6 == s1=}")

s6.update(l4)
print(f"s6.update(l4)={s6}")
s6.update(se(l2))
print(f"s6.update(se(l2))={s6}")

s7 = s1.copy()
s7 |= l4
print(f"s7 |= l4={s7}")
s7 |= se(l2)
print(f"s7 |= se(l2)={s7}")

s10 = se(l1)
s11 = se(l2)
s12 = se(l3)
s13 = se(l4)
s10.intersection_update(s11, s12, s13)
print(f"s10.intersection_update(s11,s12,s13)={s10}")
s10 = se(l1)
s10 &= s11 & s12 & s13
print(f"s10 &= s11 & s12 & s13={s10}")

s10 = se(l1)
s10.difference_update(s11, s12, s13)
print(f"s10.difference_update(s11,s12,s13)={s10}")
s10 = se(l1)
s10 -= s11 | s12 | s13
print(f"s10 -= s11 | s12 | s13={s10}")


s10 = se(l1)
s10.symmetric_difference_update(s11, s12, s13)
print(f"s10.symmetric_difference_update(s11,s12,s13)={s10}")
s10 = se(l1)
s10 ^= s11
print(f"s10 ^= s11={s10}")

s10 = se(l1)
s10.add(110)
print(f"s10.add(110)={s10}")
s10.remove(110)
print(f"s10.remove(110)={s10}")

try:
    s10.remove(110000)
    print(f"s10.discard(110000)={s10}")
except Exception as fe:
    print(fe)
s10.discard(8)
print(f"s10.discard(8)={s10}")

s10.discard(110000)
print(f"s10.discard(110000)={s10}")

print(f"{s10.pop()=}")
s10.clear()
print(f"{s10}")
#########################################################################################
s10 = se(l1)
s10.appendleft(500)
print(f"s10.appendleft(500)={s10}")

s10.extend([5000, 14500])
print(f"s10.extend([5000,14500])={s10}")

s10.extendleft([35000, 314500])
print(f"s10.extendleft([35000,314500])={s10}")


print(f"{s10.index(35000)=}")


s10.insert(3, 1114500)
print(f"s10.insert(3,1114500)={s10}")
print(f"{s10.popleft()=}")

s10.rotate(1)
print(f"s10.rotate(1)={s10}")

s10.reverse()
print(f"s10.reverse()={s10}")

# Output

s1=ScrewHashesSet([9, 0, 1, 2, 3, 4, 5, 6, 7, 8])
len(s1)=10
9 in s1=True
19 in s1=False
9 not in s1=False
19 not in s1=True
s1.isdisjoint(se(l4))=True
s1.isdisjoint(l4)=True
s1.issubset(se(l3))=False
s1 <= se(l3)=False
s1 < se(l3)=False
se(l3).issubset(s1)=True
se(l3) <= s1=True
se(l3) < s1=True
s1.issuperset(se(l3))=True
s1 >=se(l3)=True
s1 >se(l3)=True
se(l3).issuperset(s1)=False
se(l3) >= s1=False
se(l3) > s1=False
s1.union(l1,l2,l3,l4)=ScrewHashesSet([9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 10, 11, 13, 19, 20, 21, 22])
s1.union(se(l1),se(l2),se(l3),se(l4))=ScrewHashesSet([9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 10, 11, 13, 19, 20, 21, 22])
s1 | l2 | l3 | l4=ScrewHashesSet([9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 10, 11, 13, 19, 20, 21, 22])
s1 | tuple(l2) | se(l3) | se(l4)=ScrewHashesSet([9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 10, 11, 13, 19, 20, 21, 22])
[x**2 for x in s1]=[81, 0, 1, 4, 9, 16, 25, 36, 49, 64]
s1.intersection(l1,l2,l3)=ScrewHashesSet([5, 3, 4])
s1.intersection(se(l1),se(l2),se(l3))=ScrewHashesSet([5, 3, 4])
s1 & l2 & l3=ScrewHashesSet([5, 3, 4])
s1 & tuple(l2) & se(l3)=ScrewHashesSet([5, 3, 4])
s1.difference(l2,l3)=ScrewHashesSet([0, 1, 2, 8])
s1.difference(se(l2),se(l3))=ScrewHashesSet([0, 1, 2, 8])
s1 - l2 - l3=ScrewHashesSet([0, 1, 2, 8])
s1 - tuple(l2) - se(l3)=ScrewHashesSet([0, 1, 2, 8])
s1.symmetric_difference(l2,l3)=ScrewHashesSet([0, 1, 2, 8, 12, 10, 11, 13, 5, 3, 4])
s1.symmetric_difference(se(l2),se(l3))=ScrewHashesSet([0, 1, 2, 8, 12, 10, 11, 13, 5, 3, 4])
s1 ^ l2 ^ l3=ScrewHashesSet([0, 1, 2, 8, 12, 10, 11, 13, 5, 3, 4])
s1 ^ tuple(l2) ^ se(l3)=ScrewHashesSet([0, 1, 2, 8, 12, 10, 11, 13, 5, 3, 4])
s6 is s1=False
s6 == s1=True
s6.update(l4)={9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 19, 20, 21, 22}
s6.update(se(l2))={9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 19, 20, 21, 22, 12, 10, 11, 13}
s7 |= l4={9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 19, 20, 21, 22}
s7 |= se(l2)={9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 19, 20, 21, 22, 12, 10, 11, 13}
s10.intersection_update(s11,s12,s13)={}
s10 &= s11 & s12 & s13={}
s10.difference_update(s11,s12,s13)={0, 1, 2, 8}
s10 -= s11 | s12 | s13={0, 1, 2, 8}
s10.symmetric_difference_update(s11,s12,s13)={0, 1, 2, 8, 12, 10, 11, 13, 5, 3, 4, 19, 20, 21, 22}
s10 ^= s11={0, 1, 2, 8, 12, 10, 11, 13}
s10.add(110)={9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 110}
s10.remove(110)={9, 0, 1, 2, 3, 4, 5, 6, 7, 8}
110000 is not in deque
s10.discard(8)={9, 0, 1, 2, 3, 4, 5, 6, 7}
s10.discard(110000)={9, 0, 1, 2, 3, 4, 5, 6, 7}
s10.pop()=7
{}
s10.appendleft(500)={500, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8}
s10.extend([5000,14500])={500, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 5000, 14500}
s10.extendleft([35000,314500])={314500, 35000, 500, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 5000, 14500}
s10.index(35000)=1
s10.insert(3,1114500)={314500, 35000, 500, 1114500, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 5000, 14500}
s10.popleft()=314500
s10.rotate(1)={14500, 35000, 500, 1114500, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 5000}
s10.reverse()={5000, 8, 7, 6, 5, 4, 3, 2, 1, 0, 9, 1114500, 500, 35000, 14500}

```


## Examples with mutables

```python
l1 = [
    [0, 1],
    [0, 1],
    [0, 1],
    [1, 2],
    [1, 2],
    [2, 3],
    [3, 4],
    [4, 5],
    [5, 6],
    [6, 7],
    [7, 8],
    [8, 9],
]
l2 = [[2, 3], [3, 4], [4, 5], [5, 6], [11, 12], [11, 12], [12, 13], [14, 15], [15, 16]]
l3 = [[3, 4], [4, 5], [5, 6]]
l4 = [[19, 20], [21, 22], [22, 23], {24: 25}]
s1 = se(l1)
print(f"{s1=}")
print(f"{len(s1)=}")
print(f"{9 in s1=}")
print(f"{19 in s1=}")
print(f"{9 not in s1=}")
print(f"{19 not in s1=}")
print(f"{s1.isdisjoint(se(l4))=}")
print(f"{s1.isdisjoint(l4)=}")
print(f"{s1.issubset(se(l3))=}")
print(f"{s1 <= se(l3)=}")
print(f"{s1 < se(l3)=}")
print(f"{se(l3).issubset(s1)=}")
print(f"{se(l3) <= s1=}")
print(f"{se(l3) < s1=}")

print(f"{s1.issuperset(se(l3))=}")
print(f"{s1 >=se(l3)=}")
print(f"{s1 >se(l3)=}")

print(f"{se(l3).issuperset(s1)=}")
print(f"{se(l3) >= s1=}")
print(f"{se(l3) > s1=}")


print(f"{s1.union(l1,l2,l3,l4)=}")
print(f"{s1.union(se(l1),se(l2),se(l3),se(l4))=}")
print(f"{s1 | l2 | l3 | l4=}")
print(f"{s1 | tuple(l2) | se(l3) | se(l4)=}")


print(f"{s1.intersection(l1,l2,l3)=}")
print(f"{s1.intersection(se(l1),se(l2),se(l3))=}")
print(f"{s1 & l2 & l3=}")
print(f"{s1 & tuple(l2) & se(l3)=}")


print(f"{s1.difference(l2,l3)=}")
print(f"{s1.difference(se(l2),se(l3))=}")
print(f"{s1 - l2 - l3=}")
print(f"{s1 - tuple(l2) - se(l3)=}")

print(f"{s1.symmetric_difference(l2,l3)=}")
print(f"{s1.symmetric_difference(se(l2),se(l3))=}")
print(f"{s1 ^ l2 ^ l3=}")
print(f"{s1 ^ tuple(l2) ^ se(l3)=}")

s6 = s1.copy()
print(f"{s6 is s1=}")
print(f"{s6 == s1=}")

s6.update(l4)
print(f"s6.update(l4)={s6}")
s6.update(se(l2))
print(f"s6.update(se(l2))={s6}")

s7 = s1.copy()
s7 |= l4
print(f"s7 |= l4={s7}")
s7 |= se(l2)
print(f"s7 |= se(l2)={s7}")

s10 = se(l1)
s11 = se(l2)
s12 = se(l3)
s13 = se(l4)
s10.intersection_update(s11, s12, s13)
print(f"s10.intersection_update(s11,s12,s13)={s10}")
s10 = se(l1)
s10 &= s11 & s12 & s13
print(f"s10 &= s11 & s12 & s13={s10}")

s10 = se(l1)
s10.difference_update(s11, s12, s13)
print(f"s10.difference_update(s11,s12,s13)={s10}")
s10 = se(l1)
s10 -= s11 | s12 | s13
print(f"s10 -= s11 | s12 | s13={s10}")


s10 = se(l1)
s10.symmetric_difference_update(s11, s12, s13)
print(f"s10.symmetric_difference_update(s11,s12,s13)={s10}")
s10 = se(l1)
s10 ^= s11
print(f"s10 ^= s11={s10}")

s10 = se(l1)
s10.add(110)
print(f"s10.add(110)={s10}")
s10.remove(110)
print(f"s10.remove(110)={s10}")

try:
    s10.remove(110000)
    print(f"s10.discard(110000)={s10}")
except Exception as fe:
    print(fe)
s10.discard(8)
print(f"s10.discard(8)={s10}")

s10.discard(110000)
print(f"s10.discard(110000)={s10}")

print(f"{s10.pop()=}")
s10.clear()
print(f"{s10}")
#########################################################################################
s10 = se(l1)
s10.appendleft(500)
print(f"s10.appendleft(500)={s10}")

s10.extend([5000, 14500])
print(f"s10.extend([5000,14500])={s10}")

s10.extendleft([35000, 314500])
print(f"s10.extendleft([35000,314500])={s10}")


print(f"{s10.index(35000)=}")


s10.insert(3, 1114500)
print(f"s10.insert(3,1114500)={s10}")
print(f"{s10.popleft()=}")

s10.rotate(1)
print(f"s10.rotate(1)={s10}")

s10.reverse()
print(f"s10.reverse()={s10}")


# Output 

s1=ScrewHashesSet([[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9]])
len(s1)=9
9 in s1=False
19 in s1=False
9 not in s1=True
19 not in s1=True
s1.isdisjoint(se(l4))=True
s1.isdisjoint(l4)=True
s1.issubset(se(l3))=False
s1 <= se(l3)=False
s1 < se(l3)=False
se(l3).issubset(s1)=True
se(l3) <= s1=True
se(l3) < s1=True
s1.issuperset(se(l3))=True
s1 >=se(l3)=True
s1 >se(l3)=True
se(l3).issuperset(s1)=False
se(l3) >= s1=False
se(l3) > s1=False
s1.union(l1,l2,l3,l4)=ScrewHashesSet([[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [11, 12], [12, 13], [14, 15], [15, 16], [19, 20], [21, 22], [22, 23], {24: 25}])
s1.union(se(l1),se(l2),se(l3),se(l4))=ScrewHashesSet([[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [11, 12], [12, 13], [14, 15], [15, 16], [19, 20], [21, 22], [22, 23], {24: 25}])
s1 | l2 | l3 | l4=ScrewHashesSet([[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [11, 12], [12, 13], [14, 15], [15, 16], [19, 20], [21, 22], [22, 23], {24: 25}])
s1 | tuple(l2) | se(l3) | se(l4)=ScrewHashesSet([[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [11, 12], [12, 13], [14, 15], [15, 16], [19, 20], [21, 22], [22, 23], {24: 25}])
s1.intersection(l1,l2,l3)=ScrewHashesSet([[3, 4], [4, 5], [5, 6]])
s1.intersection(se(l1),se(l2),se(l3))=ScrewHashesSet([[3, 4], [4, 5], [5, 6]])
s1 & l2 & l3=ScrewHashesSet([[3, 4], [4, 5], [5, 6]])
s1 & tuple(l2) & se(l3)=ScrewHashesSet([[3, 4], [4, 5], [5, 6]])
s1.difference(l2,l3)=ScrewHashesSet([[0, 1], [1, 2], [6, 7], [7, 8], [8, 9]])
s1.difference(se(l2),se(l3))=ScrewHashesSet([[0, 1], [1, 2], [6, 7], [7, 8], [8, 9]])
s1 - l2 - l3=ScrewHashesSet([[0, 1], [1, 2], [6, 7], [7, 8], [8, 9]])
s1 - tuple(l2) - se(l3)=ScrewHashesSet([[0, 1], [1, 2], [6, 7], [7, 8], [8, 9]])
s1.symmetric_difference(l2,l3)=ScrewHashesSet([[0, 1], [1, 2], [6, 7], [7, 8], [8, 9], [11, 12], [12, 13], [14, 15], [15, 16], [3, 4], [4, 5], [5, 6]])
s1.symmetric_difference(se(l2),se(l3))=ScrewHashesSet([[0, 1], [1, 2], [6, 7], [7, 8], [8, 9], [11, 12], [12, 13], [14, 15], [15, 16], [3, 4], [4, 5], [5, 6]])
s1 ^ l2 ^ l3=ScrewHashesSet([[0, 1], [1, 2], [6, 7], [7, 8], [8, 9], [11, 12], [12, 13], [14, 15], [15, 16], [3, 4], [4, 5], [5, 6]])
s1 ^ tuple(l2) ^ se(l3)=ScrewHashesSet([[0, 1], [1, 2], [6, 7], [7, 8], [8, 9], [11, 12], [12, 13], [14, 15], [15, 16], [3, 4], [4, 5], [5, 6]])
s6 is s1=False
s6 == s1=True
s6.update(l4)={[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [19, 20], [21, 22], [22, 23], {24: 25}}
s6.update(se(l2))={[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [19, 20], [21, 22], [22, 23], {24: 25}, [11, 12], [12, 13], [14, 15], [15, 16]}
s7 |= l4={[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [19, 20], [21, 22], [22, 23], {24: 25}}
s7 |= se(l2)={[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [19, 20], [21, 22], [22, 23], {24: 25}, [11, 12], [12, 13], [14, 15], [15, 16]}
s10.intersection_update(s11,s12,s13)={}
s10 &= s11 & s12 & s13={}
s10.difference_update(s11,s12,s13)={[0, 1], [1, 2], [6, 7], [7, 8], [8, 9]}
s10 -= s11 | s12 | s13={[0, 1], [1, 2], [6, 7], [7, 8], [8, 9]}
s10.symmetric_difference_update(s11,s12,s13)={[0, 1], [1, 2], [6, 7], [7, 8], [8, 9], [11, 12], [12, 13], [14, 15], [15, 16], [3, 4], [4, 5], [5, 6], [19, 20], [21, 22], [22, 23], {24: 25}}
s10 ^= s11={[0, 1], [1, 2], [6, 7], [7, 8], [8, 9], [11, 12], [12, 13], [14, 15], [15, 16]}
s10.add(110)={[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], 110}
s10.remove(110)={[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9]}
110000 is not in deque
s10.discard(8)={[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9]}
s10.discard(110000)={[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9]}
s10.pop()=[8, 9]
{}
s10.appendleft(500)={500, [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9]}
s10.extend([5000,14500])={500, [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], 5000, 14500}
s10.extendleft([35000,314500])={314500, 35000, 500, [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], 5000, 14500}
s10.index(35000)=1
s10.insert(3,1114500)={314500, 35000, 500, 1114500, [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], 5000, 14500}
s10.popleft()=314500
s10.rotate(1)={14500, 35000, 500, 1114500, [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], 5000}
s10.reverse()={5000, [8, 9], [7, 8], [6, 7], [5, 6], [4, 5], [3, 4], [2, 3], [1, 2], [0, 1], 1114500, 500, 35000, 14500}


```

	
```python
 |  add(self, other, /)
 |      Add an element to the ScrewHashesSet.
 |      
 |      Args:
 |          other: The element to add.
 |  
 |  append(self, other, /)
 |      Append an element to the ScrewHashesSet.
 |      
 |      Args:
 |          other: The element to append.
 |  
 |  appendleft(self, elem, /)
 |      Append an element to the beginning of the ScrewHashesSet if it is not already present.
 |      
 |      Args:
 |          elem: The element to append.
 |  
 |  clear(self)
 |      Remove all elements from the ScrewHashesSet.
 |  
 |  copy(self)
 |      Create a shallow copy of the ScrewHashesSet.
 |      
 |      Returns:
 |          ScrewHashesSet: A shallow copy of the ScrewHashesSet.
 |  
 |  difference(self, *others)
 |      Return a new ScrewHashesSet with elements that are in the current set but not in any of the other sets.
 |      
 |      Args:
 |          *others: Variable number of sets to compute the difference with.
 |      
 |      Returns:
 |          ScrewHashesSet: A new ScrewHashesSet containing the elements that are in the current set but not in any of the other sets.
 |  
 |  difference_update(self, *others)
 |      Update the current ScrewHashesSet with elements that are in the current set but not in any of the other sets.
 |      
 |      Args:
 |          *others: Variable number of sets to compute the difference with.
 |  
 |  discard(self, elem, /)
 |      Remove an element from the set if it is present.
 |      
 |      Args:
 |          elem: The element to be removed from the set.
 |  
 |  extend(self, elem, /)
 |      Extend the ScrewHashesSet by adding elements from an iterable.
 |      
 |      Args:
 |          elem: An iterable containing elements to add to the ScrewHashesSet.
 |  
 |  extendleft(self, elem, /)
 |      Extend the ScrewHashesSet by adding elements from an iterable to the beginning, if they are not already present.
 |      
 |      Args:
 |          elem: An iterable containing elements to add to the ScrewHashesSet.
 |  
 |  index(self, x, start=None, stop=None, /)
 |      Return the index of the first occurrence of an element in the ScrewHashesSet.
 |      
 |      Args:
 |          x: The element to search for.
 |          start (optional): The starting index for the search. If not provided, the search starts from index 0.
 |          stop (optional): The stopping index for the search. If not provided, the search stops at the last index.
 |      
 |      Returns:
 |          int: The index of the first occurrence of the element in the ScrewHashesSet.
 |      
 |      Raises:
 |          ValueError: If the element is not found in the ScrewHashesSet.
 |  
 |  insert(self, i, x, /)
 |      Insert an element at a specified index in the ScrewHashesSet.
 |      
 |      Args:
 |          i: The index at which to insert the element.
 |          x: The element to insert.
 |  
 |  intersection(self, *others)
 |      Return a new ScrewHashesSet with elements that are common to the current set and all the other sets.
 |      
 |      Args:
 |          *others: Variable number of sets to compute the intersection with.
 |      
 |      Returns:
 |          ScrewHashesSet: A new ScrewHashesSet containing the elements that are common to the current set and all the other sets.
 |  
 |  intersection_update(self, *others)
 |      Update the current ScrewHashesSet with elements that are common to the current set and all the other sets.
 |      
 |      Args:
 |          *others: Variable number of sets to compute the intersection with.
 |  
 |  isdisjoint(self, other, /)
 |      Check if the current set has no elements in common with the other set.
 |      
 |      Args:
 |          other: The set to compare with.
 |      
 |      Returns:
 |          bool: True if the sets are disjoint (have no elements in common), False otherwise.
 |  
 |  issubset(self, other, /)
 |      Check if every element in the current set is also in the other set.
 |      
 |      Args:
 |          other: The set to compare with.
 |      
 |      Returns:
 |          bool: True if every element in the current set is also in the other set, False otherwise.
 |  
 |  issuperset(self, other, /)
 |      Check if every element in the other set is also in the current set.
 |      
 |      Args:
 |          other: The set to compare with.
 |      
 |      Returns:
 |          bool: True if every element in the other set is also in the current set, False otherwise.
 |  
 |  pop(self)
 |      Remove and return the rightmost element from the ScrewHashesSet.
 |      
 |      Returns:
 |          object: The removed element.
 |      
 |      Raises:
 |          KeyError: If the ScrewHashesSet is empty.
 |  
 |  popleft(self)
 |      Remove and return the leftmost element from the ScrewHashesSet.
 |      
 |      Returns:
 |          The leftmost element from the ScrewHashesSet.
 |      
 |      Raises:
 |          IndexError: If the ScrewHashesSet is empty.
 |  
 |  remove(self, elem, /)
 |      Remove the specified element from the ScrewHashesSet.
 |      
 |      Args:
 |          elem: The element to remove.
 |      
 |      Raises:
 |          KeyError: If the element is not present in the ScrewHashesSet.
 |  
 |  reverse(self)
 |      Reverse the order of elements in the ScrewHashesSet.
 |  
 |  rotate(self, n=1, /)
 |      Rotate the elements in the ScrewHashesSet by a specified number of steps.
 |      
 |      Args:
 |          n (optional): The number of steps to rotate the elements. Positive values rotate to the right,
 |                        and negative values rotate to the left. The default is 1.
 |  
 |  symmetric_difference(self, *others)
 |      Compute the symmetric difference between the ScrewHashesSet and multiple other sets.
 |      
 |      Args:
 |          *others: Variable length argument list of other sets.
 |      
 |      Returns:
 |          ScrewHashesSet: A new ScrewHashesSet containing elements that are present in exactly one of the sets.
 |  
 |  symmetric_difference_update(self, *others)
 |      Update the ScrewHashesSet with the symmetric difference between itself and multiple other sets.
 |      
 |      Args:
 |          *others: Variable length argument list of other sets.
 |  
 |  union(self, *others)
 |      Compute the union of the ScrewHashesSet and multiple other sets.
 |      
 |      Args:
 |          *others: Variable length argument list of other sets.
 |      
 |      Returns:
 |          ScrewHashesSet: A new ScrewHashesSet containing all unique elements from all sets.
 |  
 |  update(self, *others)
 |      Update the ScrewHashesSet by adding elements from multiple other sets.
 |      
 |      Args:
 |          *others: Variable length argument list of other sets.
```