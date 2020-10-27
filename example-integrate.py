from pprint import pprint
import numpy as np
from utils.intg import Int_F
import warnings
warnings.filterwarnings('ignore')

f = Int_F('x^2 + 5*x - 3')
n = 15
f.integrate(from_=0, to_=6, num_pts=n, method='gauss_legendre')
print(f'integration of f = {f.sol} using {n} points')

f.visualize()
