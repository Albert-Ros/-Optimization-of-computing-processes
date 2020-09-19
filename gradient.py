import numpy as np
import pandas as pd
import scipy
from matplotlib import pylab, gridspec, pyplot as plt
import math 
 
% matplotlib inline
plt.style.use('fivethirtyeight')
def f(x1, x2):
    return np.cos(x1)**2 + np.cos(x2) ** 2
 
def grad_descent(lr, num_iter=100):
    """
    функция, которая реализует градиентный спуск в минимум для функции f от двух переменных. 
        param lr: learning rate алгоритма
        param num_iter: количество итераций градиентного спуска
    """
    global f
    # в начале градиентного спуска инициализируем значения x1 и x2 какими-нибудь числами
    x1, x2 = 1.5, -1
    # будем сохранять значения аргументов и значений функции в процессе град. спуска в переменную states
    steps = []
    
    # итерация цикла -- шаг градиентнго спуска
    for iter_num in range(num_iter):
        steps.append([x1, x2, f(x1, x2)])
        
        # чтобы обновить значения x1 и x2, нужно найти производные (градиенты) функции f по этим переменным.
        grad_x1 = math.cos(2*x1) #производная по x1
        grad_x2 = math.cos(2*x1) #производная по x2
                 
        # после того, как посчитаны производные, можно обновить веса. 
        # не забудьте про lr!
        x1 -= math.cos(2*x1) #сюда вписал производную, но не уверен, что это нужно..
        x2 -= math.cos(2*x2) #сюда вписал производную, но не уверен, что это нужно..
    return np.array(steps)
steps = grad_descent(lr=0.5, num_iter=10)
