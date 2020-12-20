from random import uniform, randint
from math import *
from tkinter.messagebox import showerror
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
import matplotlib.pyplot as plt
import matplotlib
from tkinter import StringVar
import numpy as np

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


class Bacterium:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dir = []
        self.norm = 0
        self.fitness = 0
        self.health = 0
        self.f = select_func(selected_func.get())[0]

    def diffusion(self):
        self.x = uniform(-5, 5)
        self.y = uniform(-5, 5)

    def jump(self):
        self.dir = [uniform(-0.5, 0.5), uniform(-0.5, 0.5)]
        self.norm = sqrt(self.dir[0] ** 2 + self.dir[1] ** 2)

    def swim(self):
        while self.can_swim():
            self.x += float(step.get()) * self.dir[0] / self.norm
            self.y += float(step.get()) * self.dir[1] / self.norm

    def can_swim(self):
        x = self.x + float(step.get()) * self.dir[0] / self.norm
        y = self.y + float(step.get()) * self.dir[1] / self.norm
        return self.fitness > self.f(x, y)

    def calc_fitness(self):
        self.fitness = self.f(self.x, self.y)
        self.health += self.fitness

    def clone(self):
        newBacterium = Bacterium()
        newBacterium.x = self.x
        newBacterium.y = self.y
        newBacterium.dir = self.dir
        newBacterium.norm = self.norm
        newBacterium.fitness = self.fitness
        newBacterium.health = self.health
        return newBacterium

def rotate():
    plt.show()

def calc(populationSize, numberToDiffuse, maxChemotaxis, maxReproduction, maxDiffusion, diffusionChance, step) :
    f, Z = select_func(selected_func.get())

    if populationSize % 2 != 0 :
        showerror(title="Error", message="Размер популяции ТОЛЬКО четное число!")
        return

    result = [0, 0, 0]
    colony = []

    chemotaxis = 0
    rep = 0
    diff = 0

    for i in range(populationSize):
        bacterium = Bacterium()
        bacterium.diffusion()
        bacterium.calc_fitness()
        colony.append(bacterium)

    while chemotaxis < maxChemotaxis:
        chemotaxis += 1
        step = 1 / (chemotaxis / 10)
        for b in colony:
            b.jump()
        for b in colony:
            b.swim()
            b.calc_fitness()
        if rep < maxReproduction:
            part = int(len(colony) / 2)
            colony = sorted(colony, key=lambda item: item.fitness)[:part]
            for i in range(part):
                colony.append(colony[i].clone())
            rep += 1
        if diff < maxDiffusion:
            current = 0
            while current < numberToDiffuse:
                i = randint(1, populationSize - 1)
                chance = uniform(0, 1)
                if chance < diffusionChance:
                    colony[i].diffusion()
                    current += 1
            diff += 1
        for b in colony:
            b.calc_fitness()
        colony = sorted(colony, key=lambda item: item.fitness)
        best = colony[0]
        result = [best.x, best.y, best.fitness]

    print("Result:", best.x, best.y, f(best.x, best.y))
    draw(best)

def draw(best) :
    f, Z = select_func(selected_func.get())
    ax.scatter(best.x, best.y, f(best.x, best.y), color='red', s=50, marker='o')
    lbl = "Найденный минимум\nx: " + str(best.x) + "\ny: " + str(best.y) + "\nz: " + str(f(best.x, best.y))
    tk.Label(root,text=lbl).grid(row=16, column=20, columnspan = 2)

def draw_graphic(name_func) :
    f, Z = select_func(name_func)
    plt.cla()
    ax.plot_surface(X, Y, Z(), color = "green")
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

tk.Label(root, text="Размер популяции:").grid(row = 2, column=20, columnspan = 2)
populationSize  = tk.Entry(root)
populationSize.grid(row = 3, column = 20, columnspan = 2)

tk.Label(root, text="Число особей для ликвидации и распределения:").grid(row = 4, column=20, columnspan = 2)
numberToDiffuse = tk.Entry(root)
numberToDiffuse.grid(row = 5, column = 20, columnspan = 2)

tk.Label(root, text="Максимальное число шагов хемотаксиса:").grid(row = 6, column=20, columnspan = 2)
maxChemotaxis = tk.Entry(root)
maxChemotaxis.grid(row = 7, column = 20, columnspan = 2)

tk.Label(root, text="Максимальное число шагов репродукции:").grid(row = 8, column=20, columnspan = 2)
maxReproduction  = tk.Entry(root)
maxReproduction.grid(row = 9, column = 20, columnspan = 2)

tk.Label(root, text="Максимальное число шагов ликвидации и распределения:").grid(row = 10, column=20, columnspan = 2)
maxDiffusion = tk.Entry(root)
maxDiffusion.grid(row = 11, column = 20, columnspan = 2)

tk.Label(root, text="Шанс ликвидации и распределения:").grid(row = 12, column=20, columnspan = 2)
diffusionChance = tk.Entry(root)
diffusionChance.grid(row = 13, column = 20, columnspan = 2)

tk.Label(root, text="Шаг:").grid(row = 14, column=20, columnspan = 2)
step = tk.Entry(root)
step.grid(row = 15, column = 20, columnspan = 2)

rotateBtn = tk.Button(master=root, text="Обзор", command=rotate, width = 10)
rotateBtn.grid(row = 21, column = 20, columnspan = 1)

calcBtn = tk.Button(master=root, text = "Старт", width = 10, command = 
    lambda: calc(int(populationSize.get()), int(numberToDiffuse.get()), int(maxChemotaxis.get()), 
        int(maxReproduction.get()), int(maxDiffusion.get()), float(diffusionChance.get()), float(step.get())))
calcBtn.grid(row=21, column = 21, columnspan = 1)

root.mainloop()
