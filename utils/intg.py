import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from py_expression_eval import Parser
import math
parser = Parser()

class Int_F(object):
    """
    Integrate a function f(x) from a to b
    """

    def __init__(self, f_expr):
        self.f_raw = parser.parse(f_expr)
        self. ans = None
        self.int_pts = []

    @property
    def sol(self):
        return self.ans

    def f(self, x):
        return self.f_raw.evaluate({'x': x})

    def trapeziod(self, interval, n):
        """
        order: 1
        coeffs h/2 * [1 1]
        """
        a,b = interval
        h = (b-a)/(n-1)
        x = np.linspace(a,b,n)

        self.ans = (h/2)*sum([self.f(x[i]) + self.f(x[i+1]) for i in range(0,n-1,1)])

    def simpsons(self, interval,n):
        """
        order: 2
        coeffs h/3 * [1 4 1]
        """
        if (n-1)%2 != 0:
            raise Exception('Number of points must be of the form 2k+1')

        a,b = interval
        h = (b-a)/(n-1)
        x = np.linspace(a,b,n)

        self.ans = (h/3)*sum([self.f(x[i]) + 4*self.f(x[i+1]) + self.f(x[i+2]) for i in range(0,n-2,2)])

    def simpsons_3_8(self, interval, n):
        """
        order: 3
        coeffs 3h/8 * [1 3 3 1]
        """
        if (n-1)%3 != 0:
            raise Exception('Number of points must be of the form 3k+1')

        a,b = interval
        h = (b-a)/(n-1)
        x = np.linspace(a,b,n)

        self.ans = (3*h/8)*sum([self.f(x[i]) + 3*self.f(x[i+1]) + 3*self.f(x[i+2]) + self.f(x[i+3]) for i in range(0,n-3,3)])

    def gauss_legendre(self, interval, n):
        """
        gauss-legendre method
        """
        legendre_poly = np.polynomial.legendre.Legendre([0]*n + [1])
        legendre_poly_diff = legendre_poly.deriv()
        roots = legendre_poly.roots()
        weight = [ 2/((1-x**2)*legendre_poly_diff(x)**2) for x in roots]

        a,b = interval
        self.ans = ((b-a)/2) * sum([weight[i]*self.f(((b-a)/2)*x + (b+a)/2) for i,x in enumerate(roots)])
        return [((b-a)/2)*x + (b+a)/2 for x in roots]

    def integrate(self, from_, to_, num_pts, method):
        """Wrapper method to integrate the function"""
        range = (from_,to_)
        n = num_pts
        assert (n >= 2)

        self.range_ = (from_, to_)

        if method.lower() == 'trap':
            self.int_pts = np.linspace(from_, to_, num_pts)
            self.trapeziod(range,n)
        elif method.lower() == 'simp':
            self.int_pts = np.linspace(from_, to_, num_pts)
            self.simpsons(range,n)
        elif method.lower() == 'simp_3/8':
            self.int_pts = np.linspace(from_, to_, num_pts)
            self.simpsons_3_8(range,n)
        elif method.lower() == 'gauss_legendre':
            self.int_pts =  self.gauss_legendre(range,n)
        else:
            raise Exception(f'method `{method}` not implemented')

    def table(self, num_pts=500):
        xs = np.linspace(*self.range_, num_pts)
        ys = [self.f(x) for x in xs]
        return xs, ys

    def visualize(self, num_pts=500):
        xs, ys = self.table(num_pts)

        plt.plot(xs, ys, c='b', zorder=2)
        plt.plot(xs, [0 for x in xs], c='k', zorder=1)
        for pt in self.int_pts:
            minpt = min(0, self.f(pt))
            maxpt = max(0,self.f(pt))
            plt.vlines( self.int_pts,
                        [min(0,self.f(x)) for x in self.int_pts],
                        [max(0,self.f(x)) for x in self.int_pts],
                        colors=['k' for _ in self.int_pts],
                        zorder=3)
        plt.show()
