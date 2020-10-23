from pprint import pprint
import numpy as np
from utils.diff import Diff_Fn
import warnings
warnings.filterwarnings('ignore')

f = Diff_Fn('5*x^2')

f.diff(order=2, x=1, h=0.01, method='backward')
print(f'f\'\'(1) = {f.sol}')

f.visualize(range=(-10,10))
