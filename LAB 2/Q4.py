from math import pi, sqrt

class Shape:
    def area(self):
        raise NotImplementedError

    def perimeter(self):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

class Line(Shape):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def area(self):
        return 0

    def perimeter(self):
        return sqrt((self.p2.x - self.p1.x) ** 2 + (self.p2.y - self.p1.y) ** 2)

    def draw(self):
        print(f"Line drawn from {self.p1} to {self.p2}")

class Triangle(Shape):
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def area(self):
        return abs(
            (self.p1.x * (self.p2.y - self.p3.y) +
             self.p2.x * (self.p3.y - self.p1.y) +
             self.p3.x * (self.p1.y - self.p2.y)) / 2
        )

    def perimeter(self):
        return (
            Line(self.p1, self.p2).perimeter() +
            Line(self.p2, self.p3).perimeter() +
            Line(self.p3, self.p1).perimeter()
        )

    def draw(self):
        print(f"Triangle drawn at points {self.p1}, {self.p2}, {self.p3}")

class Rectangle(Shape):
    def __init__(self, top_left, width, height):
        self.top_left = top_left
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    def draw(self):
        print(f"Rectangle drawn at {self.top_left} with width {self.width} and height {self.height}")

class Square(Rectangle):
    def __init__(self, top_left, side):
        super().__init__(top_left, side, side)

    def draw(self):
        print(f"Square drawn at {self.top_left} with side {self.width}")

class Circle(Shape):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def area(self):
        return pi * self.radius ** 2

    def perimeter(self):
        return 2 * pi * self.radius

    def draw(self):
        print(f"Circle drawn at center {self.center} with radius {self.radius}")

class Quadrilateral(Shape):
    def __init__(self, p1, p2, p3, p4):
        self.points = [p1, p2, p3, p4]

    def area(self):
        return (
            Triangle(self.points[0], self.points[1], self.points[2]).area() +
            Triangle(self.points[0], self.points[2], self.points[3]).area()
        )

    def perimeter(self):
        return sum(
            Line(self.points[i], self.points[(i + 1) % 4]).perimeter()
            for i in range(4)
        )

    def draw(self):
        print("Quadrilateral drawn at points:", ", ".join(str(p) for p in self.points))

class Pentagon(Shape):
    def __init__(self, points):
        self.points = points

    def area(self):
        area = 0
        for i in range(1, 4):
            area += Triangle(self.points[0], self.points[i], self.points[i + 1]).area()
        return area

    def perimeter(self):
        return sum(
            Line(self.points[i], self.points[(i + 1) % 5]).perimeter()
            for i in range(5)
        )

    def draw(self):
        print("Pentagon drawn at points:", ", ".join(str(p) for p in self.points))

if __name__ == "__main__":
    shapes = [
        Line(Point(0, 0), Point(3, 4)),
        Triangle(Point(0, 0), Point(4, 0), Point(2, 3)),
        Rectangle(Point(0, 5), 4, 3),
        Square(Point(1, 1), 4),
        Circle(Point(0, 0), 5),
        Quadrilateral(Point(0, 0), Point(4, 0), Point(5, 3), Point(1, 3)),
        Pentagon([
            Point(0, 0), Point(2, 0), Point(3, 2),
            Point(1.5, 4), Point(0, 2)
        ])
    ]

    for shape in shapes:
        shape.draw()
        print("Area:", shape.area())
        print("Perimeter:", shape.perimeter())
        print("-" * 40)
