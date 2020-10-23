import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from py_expression_eval import Parser
import math
parser = Parser()

class Diff_Fn(object):
    """Differentiate a given function at any given point"""

    def __init__(self, f_expr):
        self.f_raw = parser.parse(f_expr)
        self.n = 1
        self.h = 0.3
        self.ans = float('nan')

    def f(self, x):
        return self.f_raw.evaluate({'x': x})

    @property
    def sol(self):
        return self.ans

    def diff(self, order, x, h=0.3, method='central'):
        """
        Numerically compute nth derivative of any given function
        This is numerically VERY unstable (as the errors propogate)
        In my tests, it works reliably for n ~ 1 ... 12
        """
        # nCk
        choose = lambda n,k: 1 if k == 0 else n * choose(n-1,k-1) / k

        n = order
        self.n = n
        self.h = h
        self.method = method

        result = 0.0
        if method.lower() == 'central':
            for k in range(n+1):
                result += pow(-1,k)*choose(n,k)*self.f(x+(n/2 - k)*h)
        elif method.lower() == 'forward':
            for k in range(n+1):
                result += pow(-1,n-k)*choose(n,k)*self.f(x+(n - k)*h)
        elif method.lower() == 'backward':
            for k in range(n+1):
                result += pow(-1,k)*choose(n,k)*self.f(x-k*h)
        else:
            raise Exception(f'method `{method}` not implemented')

        self.ans = result / pow(h,n)
        return self.ans

    def visualize(self, range, num_pts=500):
        xs = np.linspace(*range, num_pts)
        y_s = [self.diff(self.n, x, self.h, self.method) for x in xs]
        ys = [self.f(x) for x in xs]

        plt.subplot(211)
        plt.plot(xs, ys, c='b', label='f')
        plt.plot(xs,[0]*len(xs), c='k', label='X-axis')
        yl = plt.gca().get_ylim()
        plt.legend(loc='upper left')

        plt.subplot(212)
        plt.plot(xs,y_s, c='r', label=f'f^({self.n})')
        plt.plot(xs,[0]*len(xs), c='k', label='X-axis')
        plt.legend(loc='upper left')
        #plt.gca().set_ylim(yl)
        plt.show()
