import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from py_expression_eval import Parser
parser = Parser()

class find_zeroes(object):
    """
    Find zeroes of an arbitrary function defined in f(x)
    methods:
        * Bisection(a,b)
        * Secant(a,b)
    """
    def __init__(self,f_expr, max_iter=50):
        self.max_iter = max_iter
        self.sols = []
        self.f_raw = parser.parse(f_expr)

    @property
    def sol(self):
        return self.sols[-1]

    @property
    def num_iter(self):
        return len(self.sols)

    def f(self, x):
        return self.f_raw.evaluate({'x': x})

    def f_(self, x, eps=pow(10,-4)):
        return (self.f(x+eps) - self.f(x-eps)) / (2*eps)

    def stop(self, x_prev, x_curr, tol, method):
        """
        Specify stop condition:
        options are abs, rel, func
        abs: Use absolute error to terminate i.e terminate when:
            |x_{n} - x_{n-1}| < tol
        rel: Use relative error to terminate i.e terminate when:
            |x_{n} - x_{n-1}| / | x_{n-1} | < tol
        func: Use the given function to terminate i.e terminate when:
            | f(x_{n}) | < tol

        Arguements:
            * x_prev (float): solution of previous iteration
            * x_curr (float): solution of current iteration
            * tol    (float): required tolerance level
            * method   (str): (='rel') The method to use. One of 'abs', 'rel' or 'func'

        Returns:
            True if stop condition is satisfied (Algorithm should stop)
            False otherwise
        """

        if self.num_iter > self.max_iter:
            return True

        if method == 'abs':
            if np.abs(x_curr-x_prev) < tol:
                return True
        elif method == 'func':
            if np.abs(self.f(x_curr)) < tol:
                return True
        else:
            if np.abs((x_curr-x_prev)/x_prev) < tol:
                return True
        return False

    def bisection(self, a, b, tol, stopmethod):
        """
        Bisection method:

        Halve the interval (a,b) successively, the interval (a,b) should contain
        atlest one root of f(x) i.e f(a)*f(b) < 0 for this method to converge

        Arguements:
            * a: left endpoint of interval
            * b: Right endpoint of interval
            * tol: accepted tolerance level
            * stopmethod: one of abs,rel,func
        """

        if not self.f(a)*self.f(b) < 0:
            raise Exception(f'f({a})*f({b}) > 0')

        x_prev = a
        x = b
        while not self.stop(x_prev, x, tol, stopmethod):
            x_prev = x
            x = (a+b)/2
            self.sols.append(x)

            if self.f(a)*self.f(x) < 0:
                b = x
            else:
                a = x

    def regula_falsi(self, a, b, tol, stopmethod):
        """
        Regula Falsi:

        Draw a line between points (a,f(a)) and (b,f(b)) and use the intersection of
        this line with y = 0 as the next approximation, the interval (a,b) should contain
        atlest one root of f(x) i.e f(a)*f(b) < 0 for this method to converge

        Arguements:
            * a: left endpoint of interval
            * b: Right endpoint of interval
            * tol: accepted tolerance level
            * stopmethod: one of abs,rel,func
        """
        self.sols = []

        if not self.f(a)*self.f(b) < 0:
            raise Exception(f'f({a})*f({b}) > 0')

        while not self.stop(a, b, tol, stopmethod):
            x = (a*self.f(b) - b*self.f(a))/(self.f(b)-self.f(a))
            self.sols.append(x)

            if self.f(a)*self.f(x) < 0:
                b = x
            else:
                a = x

    def secant(self, x0, x1, tol, stopmethod):
        """
        Secant method:

        Use the formula: x_{n} = x_{n-1} - f(x_{n-1})*(x_{n-1} - x_{n-2})/(f(x_{n-1}) - f(x_{n-2}))
        (similar to the regula falsi method, but it may not converge)

        Arguements:
            * x0: first initial approx
            * x1: second initial approx
            * tol: accepted tolerance level
            * stopmethod: one of abs,rel,func
        """
        self.sols = [x0,x1]

        while not self.stop(self.sols[-2], self.sols[-1], tol, stopmethod):
            xn_1 = self.sols[-1]
            xn_2 = self.sols[-2]
            xn = xn_1 - self.f(xn_1)*(xn_1 - xn_2)/(self.f(xn_1) - self.f(xn_2))
            self.sols.append(xn)

    def newton(self, x0, tol, stopmethod):
        """
        Newton-Raphson method:

        Given an initial approximation x_0. Construct a tangent from (x_0, f(x_0)) and set
        x_1 to bet the intersection of this tangent and the X-axis (y=0). Guarantees quadratic
        convergence in most cases

        Arguements:
            * x0: Initial approximation
            * tol: accepted tolerance level
            * stopmethod: one of abs,rel,func
        """

        self.sols.append(x0)
        self.sols.append(x0 - self.f(x0) / self.f_(x0))

        while not self.stop(self.sols[-2], self.sols[-1], tol, stopmethod):
            x = self.sols[-1]
            x_n = x - self.f(x) / self.f_(x)
            self.sols.append(x_n)

    def find(self, method, initial, tol=0.0001, stopmethod='rel'):
        """
        Wrapper method that calls an appropriate mathod
        with the correct initial parameters
        """
        self.sols = []

        if method.lower() == 'bisection':
            try:
                a,b = initial.split(',')
                a = float(a)
                b = float(b)
            except:
                raise Exception('Invalid initial data. Expected a,b')
            self.bisection(a, b, tol, stopmethod)

        elif method.lower() == 'regula-falsi':
            try:
                a,b = initial.split(',')
                a = float(a)
                b = float(b)
            except:
                raise Exception('Invalid initial data. Expected a,b')
            self.regula_falsi(a, b, tol, stopmethod)

        elif method.lower() == 'secant':
            try:
                x0,x1 = initial.split(',')
                x0 = float(x0)
                x1 = float(x1)
            except:
                raise Exception('Invalid initial data. Expected x0,x1')
            self.secant(x0, x1, tol, stopmethod)

        elif method.lower() == 'newton':
            try:
                x0 = float(initial)
            except:
                raise Exception('Invalid initial data. Expected x0')
            self.newton(x0, tol, stopmethod)
        else:
            raise Exception(f'Method "{method.lower()}" not found')

        if self.diverges():
            print(f'Answer ({self.sol}) did not converge in {self.num_iter} iterations')
            return None

        print(f'Answer is {self.sol} +- tol reached in {self.num_iter} iterations')
        print(f'Approximate Degree of Convergence: {self.approx_convergence()}')

    def approx_convergence(self):
        """
        Convergence is defined as the number 'p' such that:
        for some C > 0: e_(n+1) = C*(e_n)^p, e_n = |x_n - x_true|
        Taking the logarithm converts it to a simple linear regression problem
        log(e_(n+1)) = p*log(e^n) + log(C)
        """

        x = np.log(np.abs(np.array(self.sols)-self.sol)) # Take log of errors
        x = x[np.isfinite(x)] # remove nans and infs
        y = x[1:]
        x = x[:-1]
        m,c = np.polyfit(x,y,deg=1) # Fit a linear polynomial
        return round(m,3) # return the slope i.e 'p'

    def diverges(self):
        """
        Check if the solution diverges (ignores the first 2 values as they may be initial parameters)
        """
        y = np.diff(np.abs(np.array(self.sols[2:]) - self.sols[-1]))

        if y[np.where(y>0)].shape[0] != 0:
            return True

        return False

    def visualize(self, label_every=1):
        """
        Visualize a given solution
        Shows how the solution improved in 2 plots:
            1. On top of the original function (y vs x) (n is shown using the color Red -> Green)
            2. How just the x value changed (x vs n) (n is number of iterations)
        """
        col = plt.get_cmap('RdYlGn')(np.linspace(0, 1, len(self.sols)))

        if self.num_iter == 0:
            print('No solutions provided!')
            return

        # Draw the approximate solutions
        plt.subplot(211)
        M = np.max(np.abs(self.sols)) + 1
        x = np.linspace(-M,M,1000)
        y = np.array([self.f(x_) for x_ in x])
        plt.hlines(0,-M, M, color='k')
        plt.plot(x,y)

        for i in range(0,len(self.sols[::label_every])-label_every):
            plt.plot([self.sols[i], self.sols[i+label_every]], [self.f(self.sols[i]), self.f(self.sols[i+label_every])], color=col[i])
        for i,sol in enumerate(self.sols[::label_every]):
            plt.scatter(sol, self.f(sol), color=col[i])
            if i%label_every == 0:
                plt.gca().annotate(str(i), (sol, self.f(sol)))

        plt.subplot(313)
        n = range(len(self.sols))
        plt.plot(n,self.sols)
        plt.show()
