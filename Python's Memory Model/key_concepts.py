# ===== Objects and References =====

a = [1, 2, 3]  # Creates a list object in memory.
b = a           # 'b' references the same object as 'a'.
b.append(4)     # Modifies the shared object.

print(a)  # Output: [1, 2, 3, 4]
print(b)  # Output: [1, 2, 3, 4]


# ===== Mutable and Immutable Objects =====

x = 5   # Immutable
x += 1  # Creates a new object for 6; 'x' references it.

lst = [1, 2]  # Mutable
lst.append(3) # Modifies the same object in memory.


# ===== id() and is =====
a = [1, 2]
b = a
c = [1, 2]

print(id(a), id(b), id(c))  # 'a' and 'b' have the same id; 'c' has a different one.
print(a is b)  # True
print(a is c)  # False


# ===== Reference Counting and Garbage Collection =====
import sys

a = [1, 2, 3]
print(sys.getrefcount(a))  # Reference count for 'a'

b = a  # Increases reference count
print(sys.getrefcount(a))  # One more reference.

del b  # Decreases reference count
print(sys.getrefcount(a))


# ===== Garbage Collection (GC) =====

import gc

# Circular reference
class Node:
    def __init__(self, value):
        self.value = value
        self.ref = None

n1 = Node(1)
n2 = Node(2)
n1.ref = n2
n2.ref = n1

del n1, n2
print(gc.collect())  # Explicitly clears circular references.



