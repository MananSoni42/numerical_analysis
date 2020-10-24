from pprint import pprint
import numpy as np
from utils.diff import Diff_Fn
import warnings
warnings.filterwarnings('ignore')

f = Diff_Fn('(x-2)*(x+7)*x')

f.diff(order=1, x=7, h=0.01, method='backward')
print(f'f\'\'(1) = {f.sol}')

f.diff(order=1, x=7, h=0.01, method='central')
print(f'f\'\'(1) = {f.sol}')

f.diff(order=1, x=7, h=0.01, method='forward')
print(f'f\'\'(1) = {f.sol}')
