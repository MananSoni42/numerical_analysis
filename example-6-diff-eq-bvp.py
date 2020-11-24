import numpy as np
from utils.de import DE

# exact solution
def e_x(x):
    '''
    Given x returns e^x
    Solution of y' = y, y(0) = 1
    '''
    return np.exp(x)

coeffs = [0,1,0]
eq = DE(coeffs) # y' = 0*x + 1*y + 0
print(f'Solving y\' = {coeffs[0]}x + {coeffs[1]}y + {coeffs[2]}')
eq.init_bvp(x0=0, xn=5, boundary=[1,1,158.41]) # y(0) + y(5) = 158.41
eq.solve_bvp(h=.5)
eq.visualize(exact_sol=e_x) # can optionally give exact solution for visualization
