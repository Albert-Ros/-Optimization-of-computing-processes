from functools import partial
import numpy as np

def _obj_wrapper(func, args, kwargs, x):
    return func(x, *args, **kwargs)

def _is_feasible_wrapper(func, x):
    return np.all(func(x)>=0)

def _cons_none_wrapper(x):
    return np.array([0])

def _cons_ieqcons_wrapper(ieqcons, args, kwargs, x):
    return np.array([y(x, *args, **kwargs) for y in ieqcons])

def _cons_f_ieqcons_wrapper(f_ieqcons, args, kwargs, x):
    return np.array(f_ieqcons(x, *args, **kwargs))
    
def pso(func, lb, ub, ieqcons=[], f_ieqcons=None, args=(), kwargs={}, 
        swarmsize=100, omega=0.5, phip=0.5, phig=0.5, maxiter=100, 
        minstep=1e-8, minfunc=1e-8, debug=False, processes=1,
        particle_output=True):
   
    assert len(lb)==len(ub), 'Нижняя и верхняя границы '
    assert hasattr(func, '__call__'), 'Недействительный дескриптор функции'
    lb = np.array(lb)
    ub = np.array(ub)
    assert np.all(ub>lb), 'Все значения верхней границы должны быть больше значений нижней границы'
   
    vhigh = np.abs(ub - lb)
    vlow = -vhigh

    # Инициализируем целевую функцию
    obj = partial(_obj_wrapper, func, args, kwargs)
    
        
    # BИнициализируем алгоритм рой частиц 
    S = swarmsize
    D = len(lb)  # количество измерений каждой частицы
    x = np.random.rand(S, D)  # положения частиц
    v = np.zeros_like(x)  # скорости частиц
    p = np.zeros_like(x)  # лучшие позиции частиц
    fx = np.zeros(S)  # текущие значения функции частиц
    fs = np.zeros(S, dtype=bool)  # выполнимость каждой частицы
    fp = np.ones(S)*np.inf  # лучшие значения функции частиц
    g = []  # лучшая позиция роя
    fg = np.inf  # начальное значение наилучшей позиции роя
    
    # Инициализируем положение частицы
    x = lb + x*(ub - lb)

    # Вычислим цель и ограничения для каждой частицы
    if processes > 1:
        fx = np.array(mp_pool.map(obj, x))
        fs = np.array(mp_pool.map(is_feasible, x))
    else:
        for i in range(S):
            fx[i] = obj(x[i, :])
            fs[i] = is_feasible(x[i, :])
       
    # Сохранить лучшую позицию частицы
    i_update = np.logical_and((fx < fp), fs)
    p[i_update, :] = x[i_update, :].copy()
    fp[i_update] = fx[i_update]

    # Обновить лучшую позицию роя
    i_min = np.argmin(fp)
    if fp[i_min] < fg:
        fg = fp[i_min]
        g = p[i_min, :].copy()
    else:
        # Задаем Отправную начальная точка роя частиц
        g = x[0, :].copy()
       
    # Инициализируем скорость частицы
    v = vlow + np.random.rand(S, D)*(vhigh - vlow)
       
    # Итерируем до тех пор, пока не будет выполнен критерий завершения 
    it = 1
    while it <= maxiter:
        rp = np.random.uniform(size=(S, D))
        rg = np.random.uniform(size=(S, D))

        # Обновление скорости частиц
        v = omega*v + phip*rp*(p - x) + phig*rg*(g - x)
        # Обновление положения частиц
        x = x + v
        # Исправление для связанных нарушений гарниц
        maskl = x < lb
        masku = x > ub
        x = x*(~np.logical_or(maskl, masku)) + lb*maskl + ub*masku

        # Обновление цели и ограничения
        if processes > 1:
            fx = np.array(mp_pool.map(obj, x))
            fs = np.array(mp_pool.map(is_feasible, x))
        else:
            for i in range(S):
                fx[i] = obj(x[i, :])
                fs[i] = is_feasible(x[i, :])

        # Сохраняем лучшую позицию частицы
        i_update = np.logical_and((fx < fp), fs)
        p[i_update, :] = x[i_update, :].copy()
        fp[i_update] = fx[i_update]

        # Сравните лучшую позицию роя с текущей позицией
        i_min = np.argmin(fp)
        if fp[i_min] < fg:
            if debug:
                print(' Новое лучшее для роя на итерациях {:}: {:} {:}'\
                    .format(it, p[i_min, :], fp[i_min]))

            p_min = p[i_min, :].copy()
            stepsize = np.sqrt(np.sum((g - p_min)**2))

            if np.abs(fg - fp[i_min]) <= minfunc:
                print('Остановка поиска: лучшая цель роя изменилась менее чем {:}'\
                    .format(minfunc))
                if particle_output:
                    return p_min, fp[i_min], p, fp
                else:
                    return p_min, fp[i_min]
            elif stepsize <= minstep:
                print('Остановка поиска: изменение лучшей позиции роя меньше чем {:}'\
                    .format(minstep))
                if particle_output:
                    return p_min, fp[i_min], p, fp
                else:
                    return p_min, fp[i_min]
            else:
                g = p_min.copy()
                fg = fp[i_min]

        if debug:
            print(' Лучше всего после итерации {:}: {:} {:}'.format(it, g, fg))
        it += 1

    print('Остановка поиска: достигнуто максимальное количество итераций --> {:}'.format(maxiter))
    
    if not is_feasible(g):
        print("Оптимизация НЕ ДОСТИГНУТА !!!!!!!")
    if particle_output:
        return g, fg, p, fp
    else:
        return g, fg
