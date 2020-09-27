import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.misc import derivative

class Poly(object):
    """
    Class to represent polynomials
    Represent polynomials as a list of coefficient
    eg:
    |     P(x)     |  function call |
    |--------------|----------------|
    | x^2 -2x + 3  | Poly([1,-2,3]) |
    | x^2 - 4      | Poly([2,0,-4]) |
    """

    def __init__(self, coeffs):
        self.coeffs = coeffs

    def at(self, x):
        """Evaluate the given polynomial at a point x"""
        result = 0
        for coeff in self.coeffs:
            result = x * result + coeff
        return result

    def __add__(self, other):
        """Add 2 polynomials"""
        coeff1 = self.coeffs
        coeff2 = other.coeffs
        l1 = len(coeff1)
        l2 = len(coeff2)

        if l1 > l2:
            coeff2 = [0]*(l1-l2) + coeff2
        elif l1 < l2:
            coeff1 = [0]*(l2-l1) + coeff1

        assert( len(coeff1) == len(coeff2) )
        return Poly([coeff1[i] + coeff2[i] for i in range(len(coeff1))])

    def scalar_mult(self, scalar):
        """Multiply polynomial by given scalar """
        self.coeffs = [scalar*coeff for coeff in self.coeffs]

    def __mul__(self, other):
        """multiply 2 polynomials"""
        res = [0]*(len(self.coeffs)+len(other.coeffs)-1)
        for o1,i1 in enumerate(self.coeffs):
            for o2,i2 in enumerate(other.coeffs):
                res[o1+o2] += i1*i2
        return Poly(res)

class Points(object):
    """
    Interpolote a polynomial f(x) from a table of (x,f(x))
    Error visualization is also available
    """
    def __init__(self, x, fx, fx_=None):
        self.x = x
        self.fx = fx
        self.fx_ = fx_
        self.pol = Poly([0])

    @property
    def sol(self):
        return self.pol.coeffs

    def lagrange(self):
        lagrange_coeffs = []
        final_poly = Poly([0])
        for i in range(len(self.x)):
            coeff = 1
            poly = Poly([1])
            for j in range(len(self.x)):
                if j!=i:
                    coeff /= (self.x[i] - self.x[j])
                    poly = poly * Poly([1,-self.x[j]])
            coeff *= self.fx[i]

            lagrange_coeffs.append(coeff)
            poly.scalar_mult(coeff)
            final_poly = final_poly + poly

        self.lagrange_coeffs = lagrange_coeffs
        self.pol = final_poly

    def interpolate(self, method):
        """Wrapper method that calls an appropriate mathod with the correct parameters"""
        if method.lower() == 'lagrange':
            self.lagrange()

    def table(self, num_pts=500):
        """Return a table of polynomial values for plotting"""
        x_min = np.min(self.x)
        x_max  = np.max(self.x)
        poly_min = min(x_min*2, x_min/2)
        poly_max = max(x_max*2, x_max/2)
        poly_x = np.linspace(poly_min,poly_max,num_pts)
        return poly_x, [self.pol.at(x) for x in poly_x]

    def visualize(self, num_pts=500):
        """
        Visualize a given solution
        Displays the original points along with the interpolated polynomial
        """
        poly_x, poly_y = self.table(num_pts)
        plt.plot(poly_x, poly_y, c='b', zorder=1)
        plt.scatter(self.x, self.fx, c='r', zorder=2)
        plt.show()
