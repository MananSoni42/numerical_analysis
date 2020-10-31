import numpy as np
from utils.de import DE

'''
Examples

1. y' = y (sol: y = e^x) ( euler v/s modified euler)
'''


y_ = 'y'

eq = DE(y_, x0=0, y0=1)

print(f'Solving y\' = {y_}')
eq.solve(method='modified-euler', h=0.5, interval=(-5,5))

eq.visualize()
