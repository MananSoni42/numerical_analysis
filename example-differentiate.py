from pprint import pprint
import numpy as np
from utils.diff import Diff_F
import warnings
warnings.filterwarnings('ignore')

f = Diff_F('5*x^2')
ord = 3
f.differentiate(order=ord, x=1, h=0.01, method='backward')
tick = '\''
print(f'f{"".join([tick]*ord)}(1) = {f.sol}')
f.visualize(range=(-10,10))
