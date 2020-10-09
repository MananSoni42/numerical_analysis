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

    def __str__(self):
        n = len(self.coeffs)
        poly = f'{self.coeffs[0]}x^{n-1}'
        for i in range(1,n):
            if self.coeffs[i] >= 0:
                poly += f' + {self.coeffs[i]} x^{n-1-i}'
            else:
                poly += f' - {-self.coeffs[i]} x^{n-1-i}'

        if n > 1:
            if self.coeffs[-1] >= 0:
                poly += f' + {self.coeffs[i]}'
            else:
                poly += f' - {-self.coeffs[i]}'
        return poly

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

        assert (len(self.x) == len(self.fx))
        if fx_:
            assert (len(self.x) == len(self.fx_))

    @property
    def sol(self):
        return self.pol.coeffs

    def f_(self, f, n, x):
        """
        Numerically compute nth derivative of any given function
        This is numerically VERY unstable, please do not change the h value
        Works reliably for n < 15

        Inputs:
        * f: function
        * n: order of derivative
        * x: point at which to evaluate the derivative
        """

        # nCk
        choose = lambda n,k: 0 if k == 0 else n * choose(n-1,k-1) / k

        h = 0.3
        result = f(x+(n/2)*h)
        for k in range(1,n+1):
            result  += pow(-1,k)*choose(n,k)*f(x+(n/2 - k)*h)
        return result / pow(h,n)

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

        self.coeffs = lagrange_coeffs
        self.pol = final_poly

    def newton_divided_diff(self):
        newton_coeffs = []
        final_poly = Poly([0])

        delf = lambda lst: self.fx[lst[0]] if len(lst) == 1 else (delf(lst[1:])-delf(lst[:-1]))/(self.x[lst[-1]] - self.x[lst[0]])

        lst = []
        poly = Poly([1])
        for i in range(len(self.x)):
            if i > 0:
                poly = poly * Poly([1,-self.x[i-1]])
            lst.append(i)
            coeff = delf(lst)

            temp_poly = Poly(poly.coeffs)
            temp_poly.scalar_mult(coeff)

            final_poly = final_poly + temp_poly
            newton_coeffs.append(coeff)

        self.coeffs = newton_coeffs
        self.pol = final_poly

    def interpolate(self, method):
        """Wrapper method that calls an appropriate mathod with the correct parameters"""
        if method.lower() == 'lagrange':
            self.lagrange()
        elif method.lower() == 'newton':
            self.newton_divided_diff()

    def table(self, num_pts=500):
        """Return a table of polynomial values for plotting"""
        x_min = np.min(self.x)
        x_max  = np.max(self.x)
        poly_min = min(x_min*2, x_min/2)
        poly_max = max(x_max*2, x_max/2)
        poly_x = np.linspace(poly_min,poly_max,num_pts)
        return poly_x, [self.pol.at(x) for x in poly_x]

    def error_table(self, actual_f, eps, xs):
        n = len(self.x)
        error_base = self.f_(actual_f, n+1, eps)
        errors = []
        for xval in xs:
            error = error_base
            for x in self.x:
                error *= (xval-x)/np.math.factorial(n+1)
            errors.append(error)
        return errors

    def visualize(self, actual_f, eps, num_pts=500):
        """
        Visualize a given solution
        Displays the original points along with the interpolated polynomial
        """
        poly_x, poly_y = self.table(num_pts)
        error_y = self.error_table(actual_f, eps, poly_x)
        plt.plot(poly_x, poly_y, c='b', zorder=1, label='intepolating polynomial')
        plt.scatter(self.x, self.fx, c='r', zorder=2, label='original data')
        plt.legend(loc="upper left")
        plt.show()
