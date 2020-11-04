import numpy as np
from utils.de import DE

'''
Examples

1. y' = y; y(0) = 1; (-3,8) (euler)
2.
'''


y_ = 'y'

eq = DE(y_, y0=1) # y(0) = y0

print(f'Solving y\' = {y_}')
#eq.solve(method='adaptive-euler', tol=0.6, xn=5)
q.solve(method='modified-euler', h=0.5, xn=5) # solve from 0 to xn

eq.visualize()
