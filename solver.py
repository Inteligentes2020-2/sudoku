import copy
from queue import PriorityQueue


# Creating Base Class
import numpy as np


class State(object):
    def __init__(self, value, parent, start=0, goal=0):
        self.children = []
        self.parent = parent
        self.value = value
        self.dist = 0
        if parent:
            self.start = parent.start
            self.goal = parent.goal
            self.path = parent.path[:]
            self.path.append(value)

        else:
            self.path = [value]
            self.start = start
            self.goal = goal

    def GetDistance(self):
        pass

    def CreateChildren(self):
        pass


# Creating subclass
class State_sudoku(State):
    def __init__(self, value, parent, start=0, goal=0):
        super(State_sudoku, self).__init__(value, parent, start, goal)
        self.dist = self.GetDistance()

    def GetDistance(self):
        dist = 81 - getFilled(self.value)
        return dist

    def CreateChildren(self):
        if not self.children:
            for i in range(1, 10):
                possible, val = fillNext(self.value, i)
                if possible:
                    child = State_sudoku(val, self)
                    self.children.append(child)


# Creating a class that hold the final magic
class A_Star_Solver:
    def __init__(self, start, goal):
        self.path = []
        self.vistedQueue = []
        self.priorityQueue = PriorityQueue()
        self.start = start
        self.goal = goal

    def Solve(self):
        startState = State_sudoku(self.start, 0, self.start, self.goal)

        count = 0
        self.priorityQueue.put((0, count, startState))
        while not self.path and self.priorityQueue.qsize():
            closesetChild = self.priorityQueue.get()[2]
            closesetChild.CreateChildren()
            self.vistedQueue.append(closesetChild.value)
            for child in closesetChild.children:
                if not any(np.array_equal(child.value, i) for i in self.vistedQueue):
                    count += 1
                    if not child.dist:
                        self.path = child.path
                        break
                    self.priorityQueue.put((child.dist, count, child))
        if not self.path:
            print("Goal Of  is not possible !" + self.goal)
        return self.path


def getFilled(grid):
    k = 0
    for i in range(9):
        for j in range(9):
            if grid[i, j] != 0:
                k += 1
    return k


def fillNext(grid, k):
    next = copy.deepcopy(grid)
    for i in range(9):
        for j in range(9):
            if grid[i, j] == 0:
                if isValid(grid, i, j, k):
                    next[i, j] = k
                    return True, next
                else:
                    return False, next
    return False, next


def isValid(grid, i, j, e):
    rowOk = all([e != grid[i][x] for x in range(9)])
    if rowOk:
        columnOk = all([e != grid[x][j] for x in range(9)])
        if columnOk:
            # finding the top left x,y co-ordinates of the section containing the i,j cell
            secTopX, secTopY = 3 * (i // 3), 3 * (j // 3)  # floored quotient should be used here.
            for x in range(secTopX, secTopX + 3):
                for y in range(secTopY, secTopY + 3):
                    if grid[x][y] == e:
                        return False
            return True
    return False


def solve(grid):
    a = A_Star_Solver(grid, 0)
    a.Solve()
    for i in range(len(a.path)):
        print("{0}){1}\n".format(i, a.path[i]))
    return a.path[-1]
