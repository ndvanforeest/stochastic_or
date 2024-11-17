from dataclasses import dataclass, field


@dataclass
class MyBaseClass:
    name: str
    age: int = field(default=0, init=False)


@dataclass
class MySubClass(MyBaseClass):
    height: float
    weight: float


# Create an instance of the subclass using named arguments
obj = MySubClass(name="John", height=180.0, weight=75.0)

# Access the attributes
print(obj.name)  # Output: John
print(obj.age)  # Output: 0 (default value)
print(obj.height)  # Output: 180.0
print(obj.weight)  # Output: 75.0
quit()


import heapq
from dataclasses import dataclass
from heapq import heappop, heappush

x = (1, 5)
y = (2, 3)
z = (1, 4)

print(x < y)
print(x < z)
quit()


@dataclass
class Student:
    age: int
    name: str

    def __lt__(self, other):
        # return self.name <= other.name
        return self.age < other.age


students = [
    Student(25, "Cynthia"),
    Student(21, "James"),
    Student(20, "Peter"),
    Student(18, "Clair"),
    Student(14, "Jim"),
]

heapq.heapify(students)
while students:
    s = heappop(students)
    # print(s.name, s.age)
    print(s.age)

quit()

heap = []


heappush(heap, (25, "Cynthia"))
heappush(heap, (21, "James"))
heappush(heap, (20, "Pete"))
heappush(heap, (18, "Clair"))
heappush(heap, (14, "Jim"))

print(heappop(heap))
print(heappop(heap))
print("Add Zoran")
heappush(heap, (23, "Zoran"))

while heap:
    e = heappop(heap)
    print(e)


quit()
