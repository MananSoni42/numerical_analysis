from pprint import pprint
import numpy as np
from utils.zeroes import find_zeroes
import warnings
warnings.filterwarnings('ignore')

# Initialize with zeroes
ans = find_zeroes("(x-1)*(x+6)")

# ans.find(method='bisection', initial='-1,10', tol=0.001, stopmethod='rel')
# ans.find(method='regula-falsi', initial='-1,10', tol=0.001, stopmethod='rel')
# ans.find(method='secant', initial='-100,-50', tol=0.001, stopmethod='rel')
ans.find(method='newton', initial='500', tol=0.001, stopmethod='rel')

ans.visualize()
