from pprint import pprint
import numpy as np
from utils.lineq import Solver
import warnings
warnings.filterwarnings('ignore')

A = [[-1,  2, -5],
     [ 1, -5,  3],
     [ 4,  2,  1]]

b = [-10,4,7]

lineq = Solver(A,b)
lineq.find_solution(method='gauss-seidel', x0=[1,0,1])

print('A is diagonally dominant: ', lineq.is_diag(lineq.A_orig))
print('transformed A is diagonally dominant: ', lineq.is_diag(lineq.A))
print('Approximate solution: ', lineq.sol)
print('Exact solution: ', lineq.exact_sol()) # Not computationally feasible for very large matrices
print(lineq.order)
