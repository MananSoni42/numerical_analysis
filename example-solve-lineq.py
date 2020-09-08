from pprint import pprint
import numpy as np
from utils.lineq import Solver
import warnings
warnings.filterwarnings('ignore')

A = [[2, 1, 2],
     [3, -3, -1],
     [1, -2,  3]]

b = [-1,5,6]

lineq = Solver(A,b)
lineq.find_solution(method='jacobi', x0=[1,0,1])

print('A is diagonally dominant:', lineq.is_diag(lineq.A_orig))
print('transformed A is diagonally dominant:', lineq.is_diag(lineq.A))
print('')
print('Exact solution:                   ', lineq.exact_sol().T) # Not computationally feasible for very large matrices
print('Solution using Gauss elimination: ', lineq.gauss_elim().T) # Not computationally feasible for very large matrices
print('Approximate solution:             ', lineq.sol.T)
