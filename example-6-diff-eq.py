import numpy as np
from utils.de import DE

# exact solution
def e_x(x):
    '''
    Given x returns e^x
    Solution of y' = y, y(0) = 1
    '''
    return np.exp(x)

# IVP example
def ivp_example():
    y_ = 'y'
    eq = DE(y_)
    print(f'Solving y\' = {y_}')
    eq.init_ivp(x0=0, y0=1) # y(x0) = x0
    eq.solve_ivp(method='milne-pc', h=0.1, interval=(0,5), tol=0.1) # solve from 0 to 5
    eq.visualize(exact_sol=e_x) # can optionally give exact solution for visualization

# BVP example
def bvp_example():
    coeffs = [0,1,0]
    eq = DE(coeffs) # y' = 0*x + 1*y + 0
    print(f'Solving y\' = {coeffs[0]}x + {coeffs[1]}y + {coeffs[2]}')
    eq.init_bvp(x0=0, xn=5, boundary=[1,1,158.41]) # y(0) + y(5) = 158.41
    eq.solve_bvp(h=.5)
    eq.visualize(exact_sol=e_x) # can optionally give exact solution for visualization

#ivp_example()
bvp_example()
