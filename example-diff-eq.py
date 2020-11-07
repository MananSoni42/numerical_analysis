import numpy as np
from utils.de import DE

def e_x(x):
    '''
    Given x returns e^x
    Solution of y' = y, y(0) = 1
    '''
    return np.exp(x)

y_ = 'y'

eq = DE(y_, x0 = 0, y0=1) # y(0) = y0

print(f'Solving y\' = {y_}')
eq.solve(method='milne-pc', h=0.1, interval=(0,5), tol=0.1) # solve from 0 to 5

eq.visualize(exact_sol=e_x) # can optionally give exact solution for visualization
