import random
from deap import base
from deap import creator
from deap import tools

#creator - фабрика классов - позволит создавать новые классы во время выполнения
#Класс FitnessMax наследует Fitness класс deap.base модуля и содержит атрибут веса в виде кортежа.

creator.create("FitnessMax", base.Fitness, weights=(1.0,))

#Класс Individual наследует класс list содержащий FitnessMax класс в своем атрибуте пригодности. 

creator.create("Individual", list, fitness=creator.FitnessMax)

# Создадим панель инструментов

# Все объекты: индивидуум, популяция,функции, операторы и аргументы будут храниться в контейнере с именем Toolbox. 
# Методы register()и unregister для добавления и удаления содержимого.
# регистрируем функцию генерации toolbox.attr_bool().
# Двумя функции инициализации individual()и population(). toolbox.attr_bool() создадим экземпляр популяции.
# Индивиды создаем с помощью функции initRepeat().

toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, 
toolbox.attr_bool, 20)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Функция оценки 
# Возвращаемое значение имеет длину, равную количеству целей (весов).

def evalOneMax(individual):
    return sum(individual),

# Генетические операторы, необходимых для эволюции.

# Мутацию зададим с вероятностью в атрибуте indpb.

toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.3)
toolbox.register("select", tools.selTournament, tournsize=3)

# Создаем экземпляр популяции, с помощью метода population().

# pop будет состоять из 20 хромосом.

def main():
    pop = toolbox.population(n=20)
 
# Оценка новой популяции

# Метод map()выполняет оценочную функцию индивида, а затем назначает его соответствующую пригодность.

    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    # P1  вероятность, с которой два индивида будут пересекаться 
    # P2 вероятность мутации индивида
   
   P1, P2 = 0.5, 0.2

# Выполнение эволюции 
# Сама эволюция будет осуществляться путем отбора, спаривания и мутации индивидов в нашей популяции.

# Извлекаем все fitness (приспособления) отдельных индивидов 
	
    fits = [ind.fitness.values[0] for ind in pop]

	# Развиваем нашу популяцию до тех пор, пока один из них не достигнет 20 или не достигнет числа поколений 1000.

    # Переменная g отслеживает количество поколений
    
	g = 0
    
    # Начинаем эволюцию
    while max(fits) < 100 and g < 1000:
        # Новое поколение
        g = g + 1
        print("-- Поколение %i --" % g)

# Первый шаг генетического алгоритма является выбор следующего поколения.

        offspring = toolbox.select(pop, len(pop))
		
# Клонирование выбранных индивидов
#Будет создан список потомков , который является точной копией выбранных индивидов.
		
        offspring = list(map(toolbox.clone, offspring))

# Выполним скрещивание и мутацию произведенных потомков с определенной вероятностью P1 и P2. 
 
        # Применим кроссовер и мутацию к потомству с определенной вероятностью CXPBи P2.
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < P1:
                toolbox.mate(child1, child2)
				
# Метод del аннулирует пригодности модифицированного потомства.
				
                del child1.fitness.values
                del child2.fitness.values
# Операторы кроссовера (или спаривания) и мутации изменяют индивидов в контейнере панели инструментов

        for mutant in offspring:
            if random.random() < P2:
                toolbox.mutate(mutant)
                del mutant.fitness.values
				
 # Так как содержание некоторых из наших потомков изменилось на последнем этапе, нужно заново оценить их пригодность. 
		
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

# заменяем старую популяцию потомством.

        pop[:] = offspring

# Проверка эффективности эволюции - вычислим и распечатаем минимальные значения

        fits = [ind.fitness.values[0] for ind in pop]

        print("  Min %s" % min(fits))
        


