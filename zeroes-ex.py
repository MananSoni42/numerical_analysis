from pprint import pprint
import numpy as np
from utils.zeroes import find_zeroes
import warnings
warnings.filterwarnings('ignore')

# Initialize with function
ans = find_zeroes("(x-1)*(x+6)")

#ans.find(method='bisection', initial=(-1,10), tol=0.001, stopmethod='rel')
#ans.find(method='regula-falsi', initial=(-1,10), tol=0.01, stopmethod='abs')
#ans.find(method='secant', initial=(100,99), tol=0.001, stopmethod='rel')
ans.find(method='newton', initial=[100], tol=0.001, stopmethod='rel')
print(f'Answer is: {round(ans.sol,5)} with an order of convergence: {ans.approx_convergence()} reached in {ans.num_iter} iterations')

ans.visualize()
