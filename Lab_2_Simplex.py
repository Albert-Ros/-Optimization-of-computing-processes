import numpy as np
from scipy.optimize import linprog
b_ub = [74,40,36] 
b_eq = [20,45,30] 
A=np.array([[7, 3,6],[4,8,2],[1,5,9]])
m, n = A.shape
c=list(np.reshape(A,n*m))# Преобразование матрицы A в список c.
A_ub= np.zeros([m,m*n])
for i in np.arange(0,m,1):# Заполнение матрицы условий –неравенств.
         for j in np.arange(0,n*m,1):
                  if i*n<=j<=n+i*n-1:
                        A_ub  [i,j]=1
A_eq= np.zeros([m,m*n])
for i in np.arange(0,m,1):# Заполнение матрицы условий –равенств.
         k=0
         for j in np.arange(0,n*m,1):
                  if j==k*n+i:
                           A_eq [i,j]=1
                           k=k+1
print(linprog(c, A_ub, b_ub, A_eq, b_eq))