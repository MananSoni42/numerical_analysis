from pprint import pprint
import numpy as np
from utils.lineq import Solver
import warnings
warnings.filterwarnings('ignore')

A = [[2,1,1],[-3,2,-2], [1,-2,3]]
b = [4,-10,7]

lineq = Solver(A,b)
lineq.find_solution(method='gauss-seidel', x0=[0,0,0])
print(lineq.sols[-1])
