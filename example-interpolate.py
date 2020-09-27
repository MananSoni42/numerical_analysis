from pprint import pprint
import numpy as np
from utils.interp import Points
import warnings
warnings.filterwarnings('ignore')

x = [-2,-1,0,1,2]
fx = [4,1,0,1,4]

f = Points(x,fx)
f.interpolate(method='lagrange')
print('lagrange coeffs: ', f.coeffs)
print('polynomial coeffs', f.sol)
f.visualize()
