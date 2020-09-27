from pprint import pprint
import numpy as np
from utils.zeroes import F
import warnings
warnings.filterwarnings('ignore')

# Initialize with function
ans = F("(x-1)*(x+6)")

#ans.find_zeroes(method='bisection', initial=(-1,10), tol=0.001, stopmethod='rel')
#ans.find_zeroes(method='regula-falsi', initial=(-1,10), tol=0.01, stopmethod='abs')
#ans.find_zeroes(method='secant', initial=(100,99), tol=0.001, stopmethod='rel')
ans.find_zeroes(method='newton', initial=[100], tol=0.001, stopmethod='rel')
print(f'Answer is: {round(ans.sol,5)} with an order of convergence: {ans.approx_convergence()} reached in {ans.num_iter} iterations')

ans.visualize()
