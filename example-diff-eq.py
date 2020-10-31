import numpy as np
from utils.de import DE

'''
Examples

1. y' = y (sol: y = e^x) ( euler and derivatives )
'''


y_ = 'y'

eq = DE(y_, x0=0, y0=1)

print(f'Solving y\' = {y_}')
#eq.solve(method='adaptive-euler', tol=0.6, interval=(-5,5))
#eq.solve(method='modified-euler', h=0.5, interval=(-5,5))

eq.visualize()
