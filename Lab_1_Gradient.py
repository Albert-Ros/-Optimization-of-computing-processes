# подключаем библиотеку для нахождения производной
from scipy.misc import derivative

# подключаем библиотеку для работы графиков
%matplotlib inline
from matplotlib import pylab as plt
import math as m

# определяем функцию
def f(x):
    return (x-10)**2

# находим производную f'(x)
derivative(f, 0)

# рисуем график функции
x = range(-5,15)
y = [f(xn) for xn in x]
plt.plot(x, y, 'b-')
plt.show()

# Градиентный спуск:

# задаем начальные значения
xn = 0 
yn = f(xn)

# создаем словарь для хранения всех найденных значений функции
Y = {xn: yn}

# шаг Градиентного Спуска
step = 0.1

# по формуле Градиентного Спуска получаем все значения x y
for _ in range(25):
    xn = xn - step*derivative(f, xn)
    yn = f(xn)
    Y[xn] = yn

Y

# отобразим найденные точки на график
plt.plot(list(Y.keys()), list(Y.values()), 'ro')
plt.show()



# создаем словарь значений, где key = х 
X = {}
for i in range(len(Y)):
    X[list(Y.values())[i]] = list(Y.keys())[i]

# выведим пару найденных минимальных X и Y 
print ('мин. Х =', min(X.items())[1])
print ('мин. Y =', min(X.items())[0])

# находим произвоную f'(x)
derivative(f, 0)

# Градиентный спуск:

# задаем начальные значения
xn = 0 
yn = f(xn)

# создаем словарь для хранения всех найденных значений функции
Y = {xn: yn}

# шаг Градиентного Спуска
step = 0.1

# по формуле Градиентного Спуска получаем все значения x y
for _ in range(25):
    xn = xn - step*derivative(f, xn)
    yn = f(xn)
    Y[xn] = yn

Y