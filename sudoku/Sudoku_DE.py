
import numpy as np
from random import randint
from random import random


class Sudoku_DE:

    def __init__(self):
        self.copy = list()
        self.board = list()
        self.generation = 20000
        self.pop_num = 100
        self.retain = 0.10





    def is_valid(self, p, row, col, value):
        x = row // 3
        y = col // 3
        board = p.copy()
        board[row][col] = 0
        s_board = board[x * 3:(x + 1) * 3, y * 3:(y + 1) * 3].copy().flatten()

        if (value > 0 and value < 10):
            if value not in board[row]:
                if value not in board.T[col]:
                    if value not in s_board:
                        return True

        return False

    def fitness(self, board):
        sum = 0

        for i in range(9):
            for j in range(9):

                if (self.copy[i, j] == 0):
                    if (self.is_valid(board, i, j, board[i][j]) == False):
                        sum += 1

        return sum

    def select_indv(self):
        board = self.copy.copy()

        for i in range(9):
            for j in range(9):

                k = 0
                while (board[i][j] == 0 and k != 100):
                    value = randint(1, 9)

                    if (self.is_valid(board, i, j, value)):
                        board[i][j] = value

                    k = k + 1
                if (board[i][j] == 0):
                    board[i][j] = randint(1, 9)

        return board

    def select_pop(self):
        return [self.select_indv() for x in range(self.pop_num)]



    def new_pop(self, pop):
        for individual in pop:
            for i in range(9):
                for j in range(9):
                    k = 0
                    while ((individual[i][j] < 1 or individual[i][j] > 9) and k != 100):
                        value = randint(1, 9)

                        if (self.is_valid(individual, i, j, value)):
                            individual[i, j] = value

                        k = k + 1
                    if (individual[i][j] < 1 or individual[i][j] > 9):
                        individual[i, j] = randint(1, 9)

        return pop

    def evolve(self, pop, k, CR=.09):
        new_gen = []

        for individual in pop:
            p1 = randint(0, len(pop) - 1)
            p2 = randint(0, len(pop) - 1)
            p3 = randint(0, len(pop) - 1)

            while (p1 == p2 or p1 == p3 or p2 == p3):
                p1 = randint(0, len(pop) - 1)
                p2 = randint(0, len(pop) - 1)
                p3 = randint(0, len(pop) - 1)

            v1 = np.array(pop[p1])
            v2 = np.array(pop[p2])
            v3 = np.array(pop[p3])

            difference = v2 - v1
            mutate = v3 + 1.8* difference
            trial = np.full((9, 9), 0)

            for i in range(9):
                for j in range(9):
                    if (CR > random()):
                        trial[i][j] = mutate[i][j]
                    else:
                        trial[i][j] = individual[i][j]

            f1 = self.fitness(trial)
            f2 = self.fitness(individual)
            if (f1 < f2):
                new_gen.append(trial)
            else:
                new_gen.append(individual)

        if ((k + 1) % 100 == 0):

            new_gen = self.new_pop(new_gen)

        return new_gen


    def replace(self, board):
        myList = [["" for col in range(9)] for row in range(9)]
        for row in range(9):
            for col in range(9):
                if board[row][col] == "":
                    myList[row][col] = 0
                else:
                    myList[row][col] = int(board[row][col])
        return np.array(myList)




    def solve_by_DE(self, board):
        self.copy = self.replace(board)

        p1 = self.select_pop()
        min = 81
        fitest = []
        pre_fitness = []
        for i in range(self.generation):
            if (i % 100 == 0):
                for ind in p1:
                    x = self.fitness(ind)
                    if (x < min):
                        min = x
                        fitest = ind

                print("the best fitness : ",min)

                if (min == 0):
                    print(" we end in generation" + str(i) )
                    break



                if min in pre_fitness:

                    graded = [(self.fitness(x), x) for x in p1]
                    graded.sort(key=lambda x: x[0])
                    graded = [x[1] for x in graded]
                    retain_length = int(len(graded) * self.retain)
                    parents = graded[:retain_length]

                    p1 = self.select_pop()

                    for s in range(retain_length):
                        p1[randint(0, self.pop_num - 1)] = parents[s]
                        pre_fitness = []
                else:
                    pre_fitness.append(min)
            p1 = self.evolve(p1, i)

        return fitest