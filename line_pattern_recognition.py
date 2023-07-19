# (!!!) NOTE: the folder with datasets must be in the same directory
import os
import matplotlib.pyplot as plt
from collections import defaultdict


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def draw_to(self, point):
        plt.plot([self.x, point.x], [self.y, point.y], "ko-", linewidth=0.5, markersize=0.6)

    def slope_to(self, that):
        # slope between this and "that" point
        try:
            return (self.y - that.y) / (self.x - that.x)
        except ZeroDivisionError:
            return float("inf")

    def __lt__(self, other):
        return self.y < other.y or (self.y == other.y and self.x < other.x)


# insertion sort
def iSort(len_arr, array):
    for i in range(1, len_arr):
        for j in range(i, 0, -1):
            if array[j] < array[j - 1]:
                old = array[j]
                array[j] = array[j - 1]
                array[j - 1] = old
            else:
                break
    return array


# get data
def getData(data_path, file):
    with open(f"{data_path}/{file}", mode="r") as f:
        data = f.readlines()
        # clear data; amount of points, array for instances
        amount, pointsArr = int(data[0]), []
        for line in data[1:]:
            xCoord, yCoord = map(int, line.split())
            pointsArr.append(Point(xCoord, yCoord))
    return amount, pointsArr


def fastAlgorithm(amount, points, data_name):
    # gradient dictionary
    grad_dict = defaultdict(list)
    # compare points by gradient
    for p in range(amount):
        for q in range(p + 1, amount):
            grad_dict[(points[p].slope_to(points[q]), points[p])] \
                += [points[p], points[q]]

    # create lines and points arrays
    for key, values in grad_dict.items():
        if len(set(values)) > 3:
            # create route array of coordinates; remove all duplicates in subarray
            # output -->
            coordinates = map(lambda a: f"{a.x, a.y}", list(dict.fromkeys(values)))
            print(" --> ".join(coordinates))
            # draw lines
            for value in values:
                key[1].draw_to(value)
    # vertical interval between datasets
    print(10*"\n")
    # plot title
    plt.title(f"{data_name} DATASET")
    plt.show()


if __name__ == "__main__":
    # get titles of files from directory with datasets
    path = "computer_vision_data"
    titles = os.listdir(path)[1:]
    # go through all datasets
    for title in titles:
        print(f"{title} DATASET")
        length, newArr = getData(path, title)
        # sort points
        newArr = iSort(length, newArr)
        fastAlgorithm(length, newArr, title)
