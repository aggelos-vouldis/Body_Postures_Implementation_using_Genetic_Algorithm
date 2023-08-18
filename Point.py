from math import sqrt, pow
from random import random
from Errors import InvalidArgumentsException
from numpy import array, dot
from numpy.linalg import norm


class Point():
    "Represents a point in the 3d space"

    def __init__(self, *xyz):
        if len(xyz) == 1:
            self.x = xyz[0][0]
            self.y = xyz[0][1]
            self.z = xyz[0][2]
        elif len(xyz) == 3:
            self.x = xyz[0]
            self.y = xyz[1]
            self.z = xyz[2]
        else:
            raise InvalidArgumentsException

    def __str__(self) -> str:
        temp_str = ''
        temp_str += f"Point: ({self.x}, {self.y}, {self.z})"
        return temp_str

    def __len__(self) -> int:
        return 3

    def set_x(self, x) -> None:
        self.x = x

    def set_y(self, y) -> None:
        self.y = y

    def set_z(self, z) -> None:
        self.z = z

    def get_x(self) -> float:
        return self.x

    def get_y(self) -> float:
        return self.y

    def get_z(self) -> float:
        return self.z

    def measure_distance(self, point) -> float:
        return sqrt(pow((self.x - point.x), 2) + pow((self.y - point.y), 2) + pow((self.z - point.z), 2))

    def measure_cosine_similarity(self, point) -> float:
        point_a = array([self.x, self.y, self.z])
        point_b = array([point.x, point.y, point.z])
        return dot(point_a, point_b) / (norm(point_a) * norm(point_b))


class TargetPoints():
    "Represents a set of 4 points in the 3d space"

    def __init__(self, *args: Point):
        if len(args) == 0:
            self.p1 = Point(random(), random(), random())
            self.p2 = Point(random(), random(), random())
            self.p3 = Point(random(), random(), random())
            self.p4 = Point(random(), random(), random())
        elif len(args) == 4:
            self.p1 = args[0]
            self.p2 = args[1]
            self.p3 = args[2]
            self.p4 = args[3]
        else:
            InvalidArgumentsException

    def __setup__(self, point_1: Point, point_2: Point, point_3: Point, point_4: Point) -> None:
        self.p1 = point_1
        self.p2 = point_2
        self.p3 = point_3
        self.p4 = point_4

    def measure_average_distance(self, target_point) -> float:
        d1 = self.p1.measure_distance(target_point.p1)
        d2 = self.p2.measure_distance(target_point.p2)
        d3 = self.p3.measure_distance(target_point.p3)
        d4 = self.p1.measure_distance(target_point.p4)

        return (d1 + d2 + d3 + d4) / 4

    def measure_cosine_similarity(self, target_point):
        array_a = array([self.p1.x, self.p1.y, self.p1.z,
                        self.p2.x, self.p2.y, self.p2.z,
                        self.p3.x, self.p3.y, self.p3.z,
                        self.p4.x, self.p4.y, self.p4.z])

        array_b = array([target_point.p1.x, target_point.p1.y, target_point.p1.z,
                        target_point.p2.x, target_point.p2.y, target_point.p2.z,
                        target_point.p3.x, target_point.p3.y, target_point.p3.z,
                        target_point.p4.x, target_point.p4.y, target_point.p4.z])

        return dot(array_a, array_b) / (norm(array_a) * norm(array_b))

    def change_p1(self, p: Point) -> None:
        self.p1 = p

    def change_p2(self, p: Point) -> None:
        self.p2 = p

    def change_p3(self, p: Point) -> None:
        self.p3 = p

    def change_p4(self, p: Point) -> None:
        self.p4 = p

    def set_i(self, i: int, value) -> None:
        if i == 0:
            self.p1.set_x(value)
        elif i == 1:
            self.p1.set_y(value)
        elif i == 2:
            self.p1.set_z(value)
        elif i == 3:
            self.p2.set_x(value)
        elif i == 4:
            self.p2.set_y(value)
        elif i == 5:
            self.p2.set_z(value)
        elif i == 6:
            self.p3.set_x(value)
        elif i == 7:
            self.p3.set_y(value)
        elif i == 8:
            self.p3.set_z(value)
        elif i == 9:
            self.p4.set_x(value)
        elif i == 10:
            self.p4.set_y(value)
        elif i == 11:
            self.p4.set_z(value)
        else:
            InvalidArgumentsException
        pass

    def get_i(self, i: int) -> float:
        if i == 0:
            return self.p1.get_x()
        elif i == 1:
            return self.p1.get_y()
        elif i == 2:
            return self.p1.get_z()
        elif i == 3:
            return self.p2.get_x()
        elif i == 4:
            return self.p2.get_y()
        elif i == 5:
            return self.p2.get_z()
        elif i == 6:
            return self.p3.get_x()
        elif i == 7:
            return self.p3.get_y()
        elif i == 8:
            return self.p3.get_z()
        elif i == 9:
            return self.p4.get_x()
        elif i == 10:
            return self.p4.get_y()
        elif i == 11:
            return self.p4.get_z()
        else:
            InvalidArgumentsException
        pass

    def change_points(self, p1: Point, p2: Point, p3: Point, p4: Point) -> None:
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4

    def something(self):
        print(self.p1.x, self.p1.y, self.p1.z,
              self.p2.x, self.p2.y, self.p2.z,
              self.p3.x, self.p3.y, self.p3.z,
              self.p4.x, self.p4.y, self.p4.z
              )

    def __str__(self) -> str:
        temp_str = ''
        temp_str += f"{self.p1}\n{self.p2}\n{self.p3}\n{self.p4}"
        return temp_str

    def __len__(self) -> int:
        return len(self.p1) + len(self.p2) + len(self.p3) + len(self.p4)


if __name__ == '__main__':
    tp1 = TargetPoints(
        Point(1, 1, 1),
        Point(2, 2, 2),
        Point(3, 3, 3),
        Point(4, 4, 4)
    )
    tp2 = TargetPoints(
        Point(1, 1, 1),
        Point(2, 2, 2),
        Point(3, 3, 3),
        Point(4, 4, 4)
    )

    cosine = tp1.measure_cosine_similarity(tp2)

    print(f"cosine: {cosine}")

    print(len(tp1))
    # print(f"distance: {distance}")
