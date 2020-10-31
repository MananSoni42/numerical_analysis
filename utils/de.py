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

    def __init__(self, y_, x0, y0):
        self.y_expr = parser.parse(y_)
        self.x0 = x0
        self.y0 = y0

    def f(self, x, y):
        return self.y_expr.evaluate({'x': x, 'y': y})

    @property
    def sol(self):
        return self.ans

    def euler(self, h , interval):
        """
        Euler's mthod
        extended to handle arbitrary intervals
        """
        self.ans = []
        a,b = interval
        x = self.x0
        y = self.y0
        while a < x:
            self.ans.append({'x': x, 'y': y})
            y = y - h * self.f(x,y)
            x = x - h

        x = self.x0
        y = self.y0
        while x < b:
            self.ans.append({'x': x, 'y': y})
            y = y + h * self.f(x,y)
            x = x + h

    def modified_euler(self, h , interval):
        """
        Modified Euler's mthod
        extended to handle arbitrary intervals
        """
        self.ans = []
        a,b = interval
        x = self.x0
        y = self.y0
        while a < x:
            self.ans.append({'x': x, 'y': y})
            y1 = y - h/2 * self.f(x,y)
            y = y1 - h/2 * self.f(x-h, y - h*y1)
            x = x - h

        x = self.x0
        y = self.y0
        while x < b:
            self.ans.append({'x': x, 'y': y})
            y1 = y + h/2 * self.f(x,y)
            y = y1 + h/2 * self.f(x+h, y + h*y1)
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
        while a < x:
            self.ans.append({'x': x, 'y': y})
            k1 = h * self.f(x, y)
            k2 = h * self.f(x - h/2, y - k1/2)
            k3 = h * self.f(x - h/2, y - k2/2)
            k4 = h * self.f(x - h, y - k3)
            y = y - (1/6) * (k1 + 2*k2+ 2*k3 + k4)
            x = x - h

        x = self.x0
        y = self.y0
        while x < b:
            self.ans.append({'x': x, 'y': y})
            k1 = h * self.f(x, y)
            k2 = h * self.f(x + h/2, y + k1/2)
            k3 = h * self.f(x + h/2, y + k2/2)
            k4 = h * self.f(x + h, y + k3)
            y = y + (1/6) * (k1 + 2*k2+ 2*k3 + k4)
            x = x + h

    def solve(self, method, h, interval):
        method = method.lower()

        if method == 'euler':
            self.euler(h, interval)
        elif method == 'modified-euler':
            self.modified_euler(h, interval)
        elif method == 'runge-kutta-4':
            self.runge_kutta(h, interval)
        else:
            raise Exception(f'Method `{method}` not implemented')


    def visualize(self):
        x = [val['x'] for val in self.ans]
        y = [val['y'] for val in self.ans]

        x,y = (list(t) for t in zip(*sorted(zip(x,y))))

        plt.plot(x, y, c='b', zorder=1, label='approximate solution')
        plt.scatter(x, y, c='r', zorder=2)
        plt.scatter(self.x0, self.y0, c='k', zorder=3)
        plt.legend(loc="upper left")
        plt.show()
