import numpy as np
import matplotlib.pyplot as plt
from py_expression_eval import Parser
parser = Parser()

class DE(object):
    """
    Solve first order Differential equations of the form:
    y' = f(x,y)

    methods:
        * Euler
        * Modified euler
        * Adaptive Euler
        * RK of order 4
    """

    def __init__(self, y_, y0):
        self.y_expr = parser.parse(y_)
        self.x0 = 0
        self.y0 = y0

    def f(self, x, y):
        return self.y_expr.evaluate({'x': x, 'y': y})

    @property
    def sol(self):
        return self.ans

    def euler(self, h , interval):
        """
        Euler's method
        extended to handle arbitrary intervals
        """
        self.ans = []
        a,b = interval
        x = self.x0
        y = self.y0
        while x <= b:
            self.ans.append({'x': x, 'y': y})
            y = y + h * self.f(x,y)
            x = x + h

    def modified_euler(self, h , interval):
        """
        Modified Euler's method
        extended to handle arbitrary intervals
        """
        self.ans = []
        a,b = interval
        x = self.x0
        y = self.y0
        while x <= b:
            self.ans.append({'x': x, 'y': y})
            y1 = y + h/2 * self.f(x,y)
            y = y1 + h/2 * self.f(x+h, y + h*y1)
            x = x + h

    def adaptive_euler(self, interval, tol):
        """
        Adaptive Euler's method
        Adjusts step size according to the tolerance provided
        extended to handle arbitrary intervals
        """
        self.ans = []
        a,b = interval

        x = self.x0
        y = self.y0
        h = 2*tol / 0.9 # initial value to the value of tolerance
        a1,a2 = (y,y)
        while x <= b:
            self.ans.append({'x': x, 'y': y})

            a1 = y + h * self.f(x,y) # euler 1 step
            ymid = y + (h/2) * self.f(x,y)
            a2 = ymid + (h/2) * self.f(x + h/2, ymid) # euler 2 step
            local_err = abs(a1-a2) / h

            while local_err > tol:
                h = 0.9 * tol * h  / local_err
                a1 = y + h * self.f(x,y) # euler 1 step
                ymid = y + (h/2) * self.f(x,y)
                a2 = ymid + (h/2) * self.f(x + h/2, ymid) # euler 2 step
                local_err = abs(a1-a2) / h

            y = 2*a2 - a1
            x = x + h

    def runge_kutta(self, h , interval):
        """
        Runge kutta method of order 4
        extended to handle arbitrary intervals
        """
        self.ans = []
        a,b = interval
        x = self.x0
        y = self.y0
        while x <= b:
            self.ans.append({'x': x, 'y': y})
            k1 = h * self.f(x, y)
            k2 = h * self.f(x + h/2, y + k1/2)
            k3 = h * self.f(x + h/2, y + k2/2)
            k4 = h * self.f(x + h, y + k3)
            y = y + (1/6) * (k1 + 2*k2+ 2*k3 + k4)
            x = x + h

    def solve(self, method, xn, h=None, tol=None):
        method = method.lower()
        interval = (0,xn)

        if method in ['euler', 'modified-euler', 'runge-kutta-4'] and not h:
            raise Exception(f'Method `{method}` requires step size `h` to be specified')
        if method in ['adaptive-euler'] and not tol:
            raise Exception(f'Method `{method}` requires a tolerance `tol` to be specified')

        if method == 'euler':
            self.euler(h, interval)
        elif method == 'modified-euler':
            self.modified_euler(h, interval)
        elif method == 'adaptive-euler':
            self.adaptive_euler(interval, tol)
        elif method == 'runge-kutta-4':
            self.runge_kutta(h, interval)
        else:
            raise Exception(f'Method `{method}` not implemented')


    def visualize(self):
        x = [val['x'] for val in self.ans]
        y = [val['y'] for val in self.ans]

        x,y = (list(t) for t in zip(*sorted(zip(x,y))))
        plt.plot(x, y, c='b', zorder=2, label='approximate solution')
        plt.scatter(x, y, c='r', zorder=3)
        plt.scatter(self.x0, self.y0, c='k', zorder=3)
        plt.legend(loc="upper left")
        plt.show()
