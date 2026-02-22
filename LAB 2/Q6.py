# C++ has Rule of 3 and Rule of 5 for manual memory management.
# Python has no such rules because it uses automatic garbage collection.
# Resource handling in Python is done via __del__(), copy methods, and with-statement.

import copy

class Demo:
    def __init__(self, value):
        self.value = value

    def __del__(self):
        print("Object destroyed automatically")

obj1 = Demo(10)

obj2 = copy.copy(obj1)
obj3 = copy.deepcopy(obj1)

print(obj1.value, obj2.value, obj3.value)
