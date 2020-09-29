from pprint import pprint
import numpy as np
from utils.interp import Points
import warnings
warnings.filterwarnings('ignore')

x = [-2,-1,0,1,2]
fx = [ 4, 3, 1, 2, 0]

actual_f = lambda x: np.exp(x)
eps = -1.5

f = Points(x,fx)
f.interpolate(method='newton')
print('coeffs: ', f.coeffs)
print('polynomial coeffs', f.sol)
f.visualize(actual_f, eps)
