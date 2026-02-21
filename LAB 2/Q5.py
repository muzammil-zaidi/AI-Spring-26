class CustomList:
    def __init__(self, size):
        self.size = size
        self.data = [None] * size
        self.count = 0

    def insert(self, value):
        if self.count == self.size:
            print("Custom List is full")
            return
        self.data[self.count] = value
        self.count += 1

    def delete(self, value):
        index = -1
        for i in range(self.count):
            if self.data[i] == value:
                index = i
                break

        if index == -1:
            print("Value not found")
            return

        for i in range(index, self.count - 1):
            self.data[i] = self.data[i + 1]

        self.data[self.count - 1] = None
        self.count -= 1

    def search(self, value):
        for i in range(self.count):
            if self.data[i] == value:
                return i
        return -1

    def display(self):
        for i in range(self.count):
            print(self.data[i], end=" ")
        print()

class Stack:
    def __init__(self, size):
        self.size = size
        self.stack = [None] * size
        self.top = -1

    def insert(self, value):
        if self.top == self.size - 1:
            print("Stack Overflow")
            return
        self.top += 1
        self.stack[self.top] = value

    def delete(self):
        if self.top == -1:
            print("Stack Underflow")
            return None
        value = self.stack[self.top]
        self.stack[self.top] = None
        self.top -= 1
        return value

    def search(self, value):
        for i in range(self.top + 1):
            if self.stack[i] == value:
                return i
        return -1

    def display(self):
        for i in range(self.top, -1, -1):
            print(self.stack[i], end=" ")
        print()

class Queue:
    def __init__(self, size):
        self.size = size
        self.queue = [None] * size
        self.front = 0
        self.rear = -1
        self.count = 0

    def insert(self, value):
        if self.count == self.size:
            print("Queue Overflow")
            return
        self.rear += 1
        self.queue[self.rear] = value
        self.count += 1

    def delete(self):
        if self.count == 0:
            print("Queue Underflow")
            return None

        value = self.queue[self.front]

        for i in range(self.rear):
            self.queue[i] = self.queue[i + 1]

        self.queue[self.rear] = None
        self.rear -= 1
        self.count -= 1
        return value

    def search(self, value):
        for i in range(self.count):
            if self.queue[i] == value:
                return i
        return -1

    def display(self):
        for i in range(self.count):
            print(self.queue[i], end=" ")
        print()

if __name__ == "__main__":

    print("=== Custom List ===")
    cl = CustomList(5)
    cl.insert(10)
    cl.insert(20)
    cl.insert(30)
    cl.display()
    cl.delete(20)
    cl.display()
    print("Search 30:", cl.search(30))
    print()

    print("=== Stack ===")
    s = Stack(5)
    s.insert(1)
    s.insert(2)
    s.insert(3)
    s.display()
    s.delete()
    s.display()
    print("Search 1:", s.search(1))
    print()

    print("=== Queue ===")
    q = Queue(5)
    q.insert(100)
    q.insert(200)
    q.insert(300)
    q.display()
    q.delete()
    q.display()
    print("Search 300:", q.search(300))
