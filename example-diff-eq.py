import numpy as np
from utils.de import DE

'''
Examples

1. y' = y; y(0) = 1; (-3,8) (euler)
'''

def e_x(x):
    '''
    Given x returns e^x
    Solution of y' = y, y(0) = 1
    '''
    return np.exp(x)

y_ = 'y'

eq = DE(y_, y0=1) # y(0) = y0

print(f'Solving y\' = {y_}')
eq.solve(method='milne-pc', h=0.1, xn=5, tol=0.1) # solve from 0 to xn

eq.visualize(exact_sol=e_x) # can optionally give exact solution for visualization
