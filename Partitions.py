import numpy as np
import math
from functools import reduce
import pandas as pd

class Partition:
    def __init__(self):
        pass

    def partitions(self, n):
        def helper(n, i, path, part):
            if n == 0:
                part.append(path)
                return
            for j in range(i, n + 1):
                helper(n - j, j, path + [j], part)

        part = []
        helper(n, 1, [], part)
        return part

    def vector_part(self, n, summands, partition):
        vector = []
        for i in range(n - summands):
            vector.append(i)
        while len(vector) != n:
            for i in range(len(partition)):
                vector.append(partition[i] + (n - summands) + i)
        return vector

    def character_vector(self, n, vector):
        flag = 0
        n_1 = [i for i in range(n)]
        characteristic = set(vector).intersection(set(n_1))
        r = n - len(characteristic)
        n_x = [n - 1 - i for i in vector]
        a_r = set(n_x).intersection(set(n_1))
        a = set(n_1).difference(set(a_r))
        a = list(a)
        b_r = [i for i in vector[-r:]]
        b = [i - n for i in b_r]
        c = []
        a.sort()
        b.sort()
        if a == b:
            flag = 1
        c.append(a)
        c.append(b)
        return c, flag, r

    def degree(self, n, characteristic):
        a_factorial = [math.factorial(i) for i in characteristic[0]]
        b_factorial = [math.factorial(i) for i in characteristic[1]]
        a_factorial, b_factorial = np.array(a_factorial, dtype='float64'), np.array(b_factorial, dtype='float64')
        a_factorial = reduce(lambda x, y: x * y, a_factorial)
        b_factorial = reduce(lambda x, y: x * y, b_factorial)
        a_factorial, b_factorial = np.array(a_factorial), np.array(b_factorial)
        a_Vander = np.vander(characteristic[0], increasing=True)
        b_Vander = np.vander(characteristic[1], increasing=True)
        a_detVander = int(np.linalg.det(a_Vander))
        b_detVander = int(np.linalg.det(b_Vander))
        power = 1
        for i in range(len(characteristic[0])):
            for j in range(len(characteristic[1])):
                power *= characteristic[0][i] + characteristic[1][j] + 1
        Z = (a_factorial * b_factorial * power) / (a_detVander * b_detVander)
        deg_Z = math.factorial(n) / Z
        return int(deg_Z)

    def create_table(self, part):
        columns = ['Натуральное число n', 'Кол-во слагаемых', 'Разбиение', 'Вектор разбиения', 'Ранг',
                   'Характеристика вектора разбиения', 'Частное степени разбиения', 'Самоассоциированные разбиения']
        data = pd.DataFrame(columns=columns)
        n = []
        summands = []
        vector = []
        character = []
        associated = []
        Z_deg = []
        rang = []

        for i in part:
            i.sort()
            n.append(sum(i))
            summands.append(len(i))

        for i in range(len(n)):
            vector.append(self.vector_part(n[i], summands[i], part[i]))

        for i in range(len(n)):
            c, a, r = self.character_vector(n[i], vector[i])
            character.append(c)
            associated.append(a)
            rang.append(r)

        for i in range(len(n)):
            Z_deg.append(self.degree(n[i], character[i]))

        data['Натуральное число n'] = n
        data['Кол-во слагаемых'] = summands
        data['Разбиение'] = part
        data['Вектор разбиения'] = vector
        data['Ранг'] = rang
        data['Характеристика вектора разбиения'] = character
        data['Частное степени разбиения'] = Z_deg
        data['Самоассоциированные разбиения'] = associated
        return data
