from pprint import pprint
import numpy as np
from utils.interp import Points
import warnings
warnings.filterwarnings('ignore')

nan = float('nan') # Use NANs to specify missing f'(x) values
x = [-2,-1,0,1,2]
fx = [ -1, 0, 1, 2, 3]
fx_ = [nan, -3, 2, -3, nan]

f = Points(x,fx,fx_)
f.interpolate()
print('lagrange coeffs: ', f.lagrange_coeffs)
print('newton coeffs: ', f.newton_coeffs)
print('polynomial: ', f.pol)
f.visualize()
