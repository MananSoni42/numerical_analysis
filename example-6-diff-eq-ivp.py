import numpy as np
from utils.de import DE

# exact solution
def e_x(x):
    '''
    Given x returns e^x
    Solution of y' = y, y(0) = 1
    '''
    return np.exp(x)

y_ = 'y'
eq = DE(y_)
print(f'Solving y\' = {y_}')
eq.init_ivp(x0=0, y0=1) # y(x0) = x0
eq.solve_ivp(method='milne-pc', h=0.1, interval=(0,5), tol=0.1) # solve from 0 to 5
eq.visualize(exact_sol=e_x) # can optionally give exact solution for visualization
