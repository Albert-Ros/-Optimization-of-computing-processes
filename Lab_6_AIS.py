from random import uniform
from math import *


def Rosenbrock(x, y):
    return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2


def Rastrigin(x, y):
    return 20 + x ** 2 + y ** 2 - 10 * (cos(2 * pi * x) + cos(2 * pi * y))


def Ackley(x, y):
    return -20*exp(-0.2*sqrt(0.5*(x**2+y**2)))-exp(0.5*(cos(2*pi*x)+cos(2*pi*y)))+e+20


def Sphere(x, y):
    return x**2 + y**2


def Himmelblau(x, y):
    return (x**2+y-11)**2 + (x+y**2-7)**2


def SinCos(x, y):
    return sin(x)*cos(y)


f = Rosenbrock

# число особей в популяции
populationSize = 50
# число приоритетных особей
numOfBest = int(populationSize / 6)
# фертильность особи (коэффициент рождаемости)
fertility = 3
# интенсивность мутации
mutationEffect = 1.0 / 20
# область мутации
area = 1.5
# максимальная итерация
maxIter = 200


class ImmuneCell:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.fitness = 0

    def randomPos(self):
        self.x = uniform(-8, 8)
        self.y = uniform(-8, 8)

    def calcFitness(self):
        self.fitness = 1 / f(self.x, self.y)

    def mutate(self):
        rate = 2**(-mutationEffect * self.fitness)
        if rate < 0.0001:
            rate = 0.0001
        self.x += uniform(-rate * area, rate * area)
        self.y += uniform(-rate * area, rate * area)

    def clone(self):
        clone = ImmuneCell()
        clone.x = self.x
        clone.y = self.y
        clone.fitness = self.fitness
        return clone


population = []

for i in range(populationSize):
    cell = ImmuneCell()
    cell.randomPos()
    cell.calcFitness()
    population.append(cell)
c = 0
while c < maxIter:

    population = sorted(population, key=lambda x: x.fitness, reverse=True)[
        :numOfBest]
    numberOfClones = populationSize - 2 * numOfBest
    for i in range(numOfBest):
        clones = []
        numberOfClones = int(numberOfClones / 2) + 1
        for j in range(numberOfClones*fertility):
            clone = population[i].clone()
            clone.mutate()
            clone.calcFitness()
            clones.append(clone)
        clones = sorted(clones, key=lambda x: x.fitness, reverse=True)
        for i in range(4):
            population.append(clones[i])
        cell = ImmuneCell()
        cell.randomPos()
        cell.calcFitness()
        population.append(cell)
        cell = ImmuneCell()
        cell.randomPos()
        cell.calcFitness()
        population.append(cell)
        if clones[0].fitness > population[i].fitness:
            population[i] = clones[0]
    population = sorted(population, key=lambda x: x.fitness, reverse=True)[
        :numOfBest]
    print("best   ", population[0].x,
          population[0].y, 1 / population[0].fitness)
    c += 1
    print(c)
