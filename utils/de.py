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
        self.y_ = y_
        self.y_expr = parser.parse(y_)
        self.x0 = 0
        self.y0 = y0

    def f(self, x, y):
        return self.y_expr.evaluate({'x': x, 'y': y})

    @property
    def sol(self):
        x = [val['x'] for val in self.ans]
        y = [val['y'] for val in self.ans]
        return (list(t) for t in zip(*sorted(zip(x,y))))

    def euler(self, h , interval):
        """
        Euler's method
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

    def adam_bashforth_2(self, h, interval):
        """
        Adom bashforth method of order 2
        Uses euler's method for initial points
        """
        self.ans = []
        a,b = interval
        x = self.x0
        y = self.y0
        order = 2
        while x <= b:
            self.ans.append({'x': x, 'y': y})
            if len(self.ans) < order:
                y = y + h * self.f(x,y)
            else:
                xp,yp = self.ans[-2]['x'], self.ans[-2]['y']
                y = y + (h/2) * (3*self.f(x,y) - self.f(xp,yp))
            x = x + h

    def adam_bashforth_3(self, h, interval):
        """
        Adom bashforth method of order 3
        Uses euler's method for initial points
        """
        self.ans = []
        a,b = interval
        x = self.x0
        y = self.y0
        order = 3
        while x <= b:
            self.ans.append({'x': x, 'y': y})
            if len(self.ans) < order:
                y = y + h * self.f(x,y)
            else:
                xp,yp = self.ans[-2]['x'], self.ans[-2]['y']
                xpp,ypp = self.ans[-3]['x'], self.ans[-3]['y']
                y = y + (h/12) * (23*self.f(x,y) - 16*self.f(xp,yp) + 5*self.f(xpp,ypp))
            x = x + h

    def adam_bashforth_4(self, h, interval):
        """
        Adom bashforth method of order 4
        Uses euler's method for initial points
        """
        self.ans = []
        a,b = interval
        x = self.x0
        y = self.y0
        order = 4
        while x <= b:
            self.ans.append({'x': x, 'y': y})
            if len(self.ans) < order:
                y = y + h * self.f(x,y)
            else:
                xp,yp     = self.ans[-2]['x'], self.ans[-2]['y']
                xpp,ypp   = self.ans[-3]['x'], self.ans[-3]['y']
                xppp,yppp = self.ans[-4]['x'], self.ans[-4]['y']
                y = y + (h/24) * (55*self.f(x,y) - 59*self.f(xp,yp) + 37*self.f(xpp,ypp) - 9*self.f(xppp, yppp))
            x = x + h

    def adam_pred_correct(self, h, interval):
        """
        Adom bashforth method (predictor - corrcector)
        Uses euler's method for initial points
        """
        self.ans = []
        a,b = interval
        x = self.x0
        y = self.y0
        order = 4
        while x <= b:
            self.ans.append({'x': x, 'y': y})
            if len(self.ans) < order:
                y = y + h * self.f(x,y)
            else:
                xp,yp     = self.ans[-2]['x'], self.ans[-2]['y']
                xpp,ypp   = self.ans[-3]['x'], self.ans[-3]['y']
                xppp,yppp = self.ans[-4]['x'], self.ans[-4]['y']
                y0 = y + (h/24) * (55*self.f(x,y) - 59*self.f(xp,yp) + 37*self.f(xpp,ypp) - 9*self.f(xppp, yppp))
                y = y + (h/24) * (9*self.f(x+h,y0) + 19*self.f(x,y) - 5*self.f(xp,yp) + self.f(xpp, ypp))
            x = x + h

    def milne_pred_correct(self, h, interval):
        """
        Milne's method (predictor - corrcector)
        Uses euler's method for initial points
        """
        self.ans = []
        a,b = interval
        x = self.x0
        y = self.y0
        order = 4
        while x <= b:
            self.ans.append({'x': x, 'y': y})
            if len(self.ans) < order:
                y = y + h * self.f(x,y)
            else:
                xp,yp     = self.ans[-2]['x'], self.ans[-2]['y']
                xpp,ypp   = self.ans[-3]['x'], self.ans[-3]['y']
                xppp,yppp = self.ans[-4]['x'], self.ans[-4]['y']
                y0 = yppp + (4*h/3) * (2*self.f(xpp,ypp) - self.f(xp,yp) + 2*self.f(x,y))
                y = yp + (h/3) * (self.f(xp,yp) + 4*self.f(x,y) + self.f(x+h,y0))
            x = x + h

    def adam_milne_pred_correct(self, h, interval, tol):
        """
        Adom milne method (predictor - corrcector)
        Uses euler's method for initial points
        Uses predictor formula till relative error < tol (or count > 50)
        """
        self.ans = []
        a,b = interval
        x = self.x0
        y = self.y0
        order = 4
        while x <= b:
            self.ans.append({'x': x, 'y': y})
            if len(self.ans) < order:
                y = y + h * self.f(x,y)
            else:
                xp,yp     = self.ans[-2]['x'], self.ans[-2]['y']
                xpp,ypp   = self.ans[-3]['x'], self.ans[-3]['y']
                xppp,yppp = self.ans[-4]['x'], self.ans[-4]['y']
                y0 = y + (h/24) * (55*self.f(x,y) - 59*self.f(xp,yp) + 37*self.f(xpp,ypp) - 9*self.f(xppp, yppp))
                y = y + (h/24) * (9*self.f(x+h,y0) + 19*self.f(x,y) - 5*self.f(xp,yp) + self.f(xpp, ypp))
                count = 1
                while abs((y-y0)/y) > tol and count < 50:
                    count += 1
                    y0 = y
                    y = y0 + (h/24) * (9*self.f(x+h,y0) + 19*self.f(x,y) - 5*self.f(xp,yp) + self.f(xpp, ypp))
            x = x + h

    def solve(self, method, xn, h=None, tol=None):
        method = method.lower()
        interval = (0,xn)

        if (xn <= 0):
            raise Exception('Right endpoint can\'t be negative')

        if method in ['euler', 'modified-euler', 'runge-kutta-4', 'adam-milne-pc'] and not h:
            raise Exception(f'Method `{method}` requires step size `h` to be specified')
        if method in ['adaptive-euler', 'adam-milne-pc'] and not tol:
            raise Exception(f'Method `{method}` requires a tolerance `tol` to be specified')

        if method == 'euler':
            self.euler(h, interval)
        elif method == 'modified-euler':
            self.modified_euler(h, interval)
        elif method == 'adaptive-euler':
            self.adaptive_euler(interval, tol)
        elif method == 'runge-kutta-4':
            self.runge_kutta(h, interval)
        elif method == 'adam-bashforth-2':
            self.adam_bashforth_2(h, interval)
        elif method == 'adam-bashforth-3':
            self.adam_bashforth_3(h, interval)
        elif method == 'adam-bashforth-4':
            self.adam_bashforth_4(h, interval)
        elif method == 'milne-pc':
            self.milne_pred_correct(h, interval)
        elif method == 'adam-bashforth-pc':
            self.adam_pred_correct(h, interval)
        elif method == 'adam-milne-pc':
            self.adam_milne_pred_correct(h, interval, tol)
        else:
            raise Exception(f'Method `{method}` not implemented')


    def visualize(self, exact_sol=None):
        x = [val['x'] for val in self.ans]
        y = [val['y'] for val in self.ans]

        x,y = (list(t) for t in zip(*sorted(zip(x,y))))
        plt.plot(x, y, c='b', zorder=2, label='approximate solution')
        plt.scatter(x, y, c='r', zorder=3)
        if exact_sol:
            ys = [exact_sol(x_) for x_ in x]
            plt.plot(x, ys, c='y', zorder=2, label='exact solution')
            plt.scatter(x, ys, c='k', zorder=3)
        plt.scatter(self.x0, self.y0, c='k', zorder=3)
        plt.legend(loc="upper left")
        plt.show()
