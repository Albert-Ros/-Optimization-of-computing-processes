import numpy as np
from random import uniform
from math import *
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
import matplotlib.pyplot as plt
import matplotlib
  
from tkinter import StringVar
import time
matplotlib.use('Agg')
matplotlib.use('TkAgg')

i = np.arange(-5, 5, 0.01)
X, Y = np.meshgrid(i, i)

def Rosenbrock(x, y):
    return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2

def Rastrigin(x, y):
    return 20 + x ** 2 + y ** 2 - 10 * (cos(2 * pi * x) + cos(2 * pi * y))

def Himmelblau(x, y):
    return (x**2+y-11)**2 + (x+y**2-7)**2

def draw_Rosenbrock():
    return (1 - X) ** 2 + 100 * (Y - X ** 2) ** 2

def draw_Rastrigin():
    return 20 + X ** 2 + Y ** 2 - 10 * (np.cos(2 * pi * X) + np.cos(2 * pi * Y))

def draw_Himmelblau():
    return (X**2+Y-11)**2 + (X+Y**2-7)**2

def select_func(name_func) :
    if name_func == "Функция Розенброка" :
        f = Rosenbrock
        Z = draw_Rosenbrock
    elif name_func == "Функция Растригина" :
        f = Rastrigin
        Z = draw_Rastrigin
    else :
        f = Himmelblau
        Z = draw_Himmelblau
    return f, Z

class Particle(object):
    def __init__(self, swarm):
        self.__currentPosition = np.random.rand(
            2) * (swarm.maxvalues - swarm.minvalues) + swarm.minvalues
        self.__localBestPosition = self.__currentPosition[:]
        self.__localBestFinalFunc = swarm.getFinalFunc(
            self.__currentPosition)
        self.__velocity = self.__getInitVelocity(swarm)

    @property
    def position(self):
        return self.__currentPosition

    @property
    def velocity(self):
        return self.__velocity

    def __getInitVelocity(self, swarm):
        minval = -(swarm.maxvalues - swarm.minvalues)
        maxval = (swarm.maxvalues - swarm.minvalues)
        return np.random.rand(2) * (maxval - minval) + minval

    def nextIteration(self, swarm):
        rnd_currentBestPosition = np.random.rand(swarm.dimension)
        rnd_globalBestPosition = np.random.rand(swarm.dimension)
        veloRatio = swarm.localVelocityRatio + swarm.globalVelocityRatio
        commonRatio = (2.0 * swarm.currentVelocityRatio /
                       (np.abs(2.0 - veloRatio - np.sqrt(veloRatio ** 2 - 4.0 * veloRatio))))
        newVelocity_part1 = commonRatio * self.__velocity
        newVelocity_part2 = (commonRatio *
                             swarm.localVelocityRatio *
                             rnd_currentBestPosition *
                             (self.__localBestPosition - self.__currentPosition))
        newVelocity_part3 = (commonRatio *
                             swarm.globalVelocityRatio *
                             rnd_globalBestPosition *
                             (swarm.globalBestPosition - self.__currentPosition))
        self.__velocity = newVelocity_part1 + newVelocity_part2 + newVelocity_part3
        self.__currentPosition += self.__velocity
        finalFunc = swarm.getFinalFunc(self.__currentPosition)
        if finalFunc < self.__localBestFinalFunc:
            self.__localBestPosition = self.__currentPosition[:]
            self.__localBestFinalFunc = finalFunc

class Swarm(object):
    def __init__(self, swarmsize, currentVelocityRatio, localVelocityRatio, globalVelocityRatio):
        self.__swarmsize = swarmsize

        self.__minvalues = np.array([-5] * 2)
        self.__maxvalues = np.array([5] * 2)

        self.__currentVelocityRatio = currentVelocityRatio
        self.__localVelocityRatio = localVelocityRatio
        self.__globalVelocityRatio = globalVelocityRatio

        self.__globalBestFinalFunc = None
        self.__globalBestPosition = None

        self.__swarm = self.__createSwarm()

    def __getitem__(self, index):
        return self.__swarm[index]

    def __createSwarm(self):
        return [Particle(self) for _ in range(self.__swarmsize)]

    def nextIteration(self):
        for particle in self.__swarm:
            particle.nextIteration(self)

    @property
    def minvalues(self):
        return self.__minvalues

    @property
    def maxvalues(self):
        return self.__maxvalues

    @property
    def currentVelocityRatio(self):
        return self.__currentVelocityRatio

    @property
    def localVelocityRatio(self):
        return self.__localVelocityRatio

    @property
    def globalVelocityRatio(self):
        return self.__globalVelocityRatio

    @property
    def globalBestPosition(self):
        return self.__globalBestPosition

    @property
    def globalBestFinalFunc(self):
        return self.__globalBestFinalFunc

    def getFinalFunc(self, position):
        finalFunc = self._finalFunc(position)
        if (self.__globalBestFinalFunc == None or finalFunc < self.__globalBestFinalFunc):
            self.__globalBestFinalFunc = finalFunc
            self.__globalBestPosition = position[:]
        return finalFunc

    def _finalFunc(self, position):
        x = position[0]
        y = position[1]
        f = select_func(selected_func.get())[0]
        return f(x, y)

    @property
    def dimension(self):
        return len(self.minvalues)

class ImmuneCell:

        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.fitness = 0
            self.f = select_func(selected_func.get())[0]

        def randomPos(self):
            self.x = uniform(-8, 8)
            self.y = uniform(-8, 8)

        def calcFitness(self):
            self.fitness = 1 / self.f(self.x, self.y)

        def mutate(self):
            rate = 2**(-float(mutationEffect.get()) * self.fitness)
            if rate < 0.0001:
                rate = 0.0001
            self.x += uniform(-rate * float(area.get()), rate * float(area.get()))
            self.y += uniform(-rate * float(area.get()), rate * float(area.get()))

        def clone(self):
            clone = ImmuneCell(self.x, self.y)
            # clone.x = self.x
            # clone.y = self.y
            clone.fitness = self.fitness
            return clone

def rotate():
    plt.show()

def calc(populationSize, numOfBest, fertility, mutationEffect, area, maxIterImun, maxIterSwarm, swarmsize) :
    currentVelocityRatio = 0.1
    localVelocityRatio = 1.0
    globalVelocityRatio = 5.0

    start_time = time.time()

    swarm = Swarm(swarmsize, currentVelocityRatio,
                localVelocityRatio, globalVelocityRatio)

    for n in range(maxIterSwarm):
        swarm.nextIteration()

    best = [swarm.globalBestPosition[0], swarm.globalBestPosition[1]]

    population = []

    for i in range(populationSize):
        cell = ImmuneCell(best[0], best[1])
        cell.calcFitness()
        population.append(cell)

    c = 0
    while c < maxIterImun:

        population = sorted(population, key=lambda x: x.fitness, reverse=True)[
            :numOfBest]
        numberOfClones = populationSize - 2 * numOfBest
        for i in range(numOfBest):
            clones = []
            numberOfClones = int(numberOfClones / 2) + 1
            for j in range(numberOfClones * fertility):
                clone = population[i].clone()
                clone.mutate()
                clone.calcFitness()
                clones.append(clone)
            clones = sorted(clones, key=lambda x: x.fitness, reverse=True)
            for i in range(4):
                population.append(clones[i])
            cell = ImmuneCell(best[0], best[1])
            cell.randomPos()
            cell.calcFitness()
            population.append(cell)
            cell = ImmuneCell(best[0], best[1])
            cell.randomPos()
            cell.calcFitness()
            population.append(cell)
            if clones[0].fitness > population[i].fitness:
                population[i] = clones[0]
        population = sorted(population, key=lambda x: x.fitness, reverse=True)[
            :numOfBest]
        c += 1

    print("Лучшая частица:", best)
    print("Результат - лучшая иммунная клетка:", population[0].x,
        population[0].y, 1 / population[0].fitness)
    print("Время: ", time.time() - start_time)

    draw(population[0])

def draw(population) :
    ax.scatter(population.x, population.y, 1 / population.fitness, color='red', s=50, marker='o')
    lbl = "Найденный минимум\nx: " + str(population.x) + "\ny: " + str(population.y) + "\nz: " + str(1 / population.fitness)
    tk.Label(root,text=lbl).grid(row=19, column=20, columnspan = 2)

def draw_graphic(name_func) :
    Z = select_func(name_func)[1]
    plt.cla()
    ax.plot_surface(X, Y, Z(), color = "grey")
    canvas.draw()


root = tk.Tk()
fig = plt.figure(dpi=100)
ax = fig.add_subplot(111, projection='3d')

canvas = FigureCanvasTkAgg(fig, master=root)

canvas.mpl_connect(
    "key_press_event", lambda event: print(f"you pressed {event.key}"))
canvas.mpl_connect("key_press_event", key_press_handler)

canvas.get_tk_widget().grid(row = 0, column = 0,rowspan=20, columnspan = 20)

toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
toolbar.update()
toolbar.grid(row=21, column=0, columnspan = 20, rowspan = 1)

selected_func = StringVar(value="Функция Розенброка")
funcs = ["Функция Розенброка", "Функция Растригина", "Функция Химмельблау"]
func_list_box = tk.OptionMenu(root, selected_func, *funcs, command = draw_graphic )
func_list_box.config(font = "times 12", width = 20)
func_list_box.grid(row = 1, column = 20, columnspan = 2)

tk.Label(root, text="Размер популяции (иммунный):").grid(row = 2, column=20, columnspan = 2)
populationSize  = tk.Entry(root)
populationSize.grid(row = 3, column = 20, columnspan = 2)

tk.Label(root, text="Число приоритетных особей:").grid(row = 4, column=20, columnspan = 2)
numOfBest = tk.Entry(root)
numOfBest.grid(row = 5, column = 20, columnspan = 2)

tk.Label(root, text="Коэффициент рождаемости:").grid(row = 6, column=20, columnspan = 2)
fertility = tk.Entry(root)
fertility.grid(row = 7, column = 20, columnspan = 2)

tk.Label(root, text="Интенсивность мутации:").grid(row = 8, column=20, columnspan = 2)
mutationEffect  = tk.Entry(root)
mutationEffect.grid(row = 9, column = 20, columnspan = 2)

tk.Label(root, text="Область мутации:").grid(row = 10, column=20, columnspan = 2)
area = tk.Entry(root)
area.grid(row = 11, column = 20, columnspan = 2)

tk.Label(root, text="Кол-во итераций (иммунный):").grid(row = 12, column=20, columnspan = 2)
maxIter = tk.Entry(root)
maxIter.grid(row = 13, column = 20, columnspan = 2)

tk.Label(root, text="Кол-во итераций (рой):").grid(row = 14, column=20, columnspan = 2)
maxIterSwarm = tk.Entry(root)
maxIterSwarm.grid(row = 15, column = 20, columnspan = 2)

tk.Label(root, text="Размер популяции (рой):").grid(row = 16, column=20, columnspan = 2)
swarmsize = tk.Entry(root)
swarmsize.grid(row = 17, column = 20, columnspan = 2)

rotateBtn = tk.Button(master=root, text="Обзор 3D", command=rotate, width = 10)
rotateBtn.grid(row = 21, column = 20, columnspan = 1)

rotateBtn = tk.Button(master=root, text="Обзор 3D", command=rotate, width = 10)
rotateBtn.grid(row = 21, column = 20, columnspan = 1)

calcBtn = tk.Button(master=root, text = "Пуск", width = 10, command = 
    lambda: calc(int(populationSize.get()), int(numOfBest.get()), int(fertility.get()), 
        float(mutationEffect.get()), float(area.get()), int(maxIter.get()), int(maxIterSwarm.get()), int(swarmsize.get())))
calcBtn.grid(row=21, column = 21, columnspan = 1)

root.mainloop()
