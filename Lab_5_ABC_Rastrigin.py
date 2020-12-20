try:
    import numpy as np
except:
    raise ImportError("Numpy module not installed.")

from Hive import Hive
from Hive import Utilities

def evaluator(vector):
    #                            n
    #       f(x) = 10*n + Sigma { x_i^2 - 10*cos(2*PI*x_i) }
    #                       i=1

    #      -5.12 <= x_i <= 5.12.

    #      global minimal f(x) = 0 at all x_i = 0.

    

    vector = np.array(vector)

    return 10 * vector.size + sum(vector*vector - 10 * np.cos(2 * np.pi * vector))


def run():

   
    ndim = int(10)
    model = Hive.BeeHive(lower = [-5.12]*ndim  ,
                         upper = [ 5.12]*ndim  ,
                         fun       = evaluator ,
                         numb_bees =  50       ,
                         max_itrs  =  100       ,)

 
    cost = model.run()


    Utilities.ConvergencePlot(cost)


    print("Fitness Value ABC: {0}".format(model.best))


if __name__ == "__main__":
    run()



