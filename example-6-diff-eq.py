import numpy as np
from utils.de import DE

def e_x(x):
    '''
    Given x returns e^x
    Solution of y' = y, y(0) = 1
    '''
    return np.exp(x)

# IVP example
y_ = 'y'
eq = DE(y_)
print(f'Solving y\' = {y_}')
eq.init_ivp(x0=0, y0=1) # y(x0) = x0
eq.solve_ivp(method='milne-pc', h=0.1, interval=(0,5), tol=0.1) # solve from 0 to 5

'''
# BVP example
eq = DE([0,1,0]) # y' = 0*x + 1*y + 0
eq.init_bvp(x0=0, xn=5, b1=[1,0,1], b2=[0,1,148.41]) # y(0) = 1, y(5) = 148.41
eq.solve_bvp(h=0.1)
'''

eq.visualize(exact_sol=e_x) # can optionally give exact solution for visualization
