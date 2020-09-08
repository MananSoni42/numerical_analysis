import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

class Solver(object):
    """
    Find the solution for the linear system Ax = b
    methods:
        * Jacobi
        * Gauss-Seidel
    """
    def __init__(self, A, b, max_iter=100, tol=0.1):
        self.A = np.array(A)
        self.b = np.array(b)
        self.n = self.A.shape[0]
        self.max_iter = max_iter - 1
        self.tol = tol
        self.sols = []

        if self.b.shape == (self.n,):
            self.b = self.b.reshape(self.b.shape[0],1)
        if (self.b.shape == (1,self.n)):
            self.b = self.b.T
        if (self.A.shape != (self.n,self.n)):
            raise Exception(f'incorrect dimensions for A: expected ({self.n},{self.n}) got ({self.A.shape})')
        if (self.b.shape != (self.n,1)):
            raise Exception(f'incorrect dimensions for b: expected ({self.n},1) got {self.b.shape}')

        self.A_orig = self.A.copy()
        self.b_orig = self.b.copy()
        self.order = np.array([i for i in range(self.n)])
        self.diag() # Try to convert A to diagonally dominant by swapping rows

    @property
    def sol(self):
        #return self.sols[-1][self.order]
        return self.sols[-1]

    @property
    def num_iter(self):
        return len(self.sols)

    def is_diag(self, A):
        return np.all([2*np.abs(A[i,i]) >= np.sum(abs(A[i,:]))  for i in range(self.n)])

    def exact_sol(self):
        return np.dot(np.linalg.inv(self.A_orig),self.b_orig)

    def gauss_elim(self):
        A = np.array(self.A_orig.copy(), dtype=np.float32)
        b = np.array(self.b_orig.copy(), dtype=np.float32)
        x = np.zeros_like(b, dtype=np.float32)

        # Reduce to REF
        for i in range(self.n):
            if abs(A[i,i]) <= 1e-3: # Zero found, swap rows
                for j in range(i+1, self.n):
                    if abs(A[i,i]) > 1e-3:
                        A[[i,j]] = A[[j,i]]
                        b[[i,j]] = b[[j,i]]
                        break
                else:
                    raise Exception('Matrix is singular')
            else:
                for j in range(i+1,self.n):
                    ratio = A[j,i]/A[i,i] # Get factor to multiply

                    A[j,:] = A[j,:] - ratio*A[i,:] # Update jth row in A
                    b[j] = b[j] - ratio*b[i] # Update jth row in b

        # Back substitution
        x[-1] = b[-1]/A[-1][-1] # last value is directly found
        for i in reversed(range(self.n-1)):
            x[i] = b[i]/A[i,i]
            for j in range(i+1,self.n):
                x[i] = x[i] - x[j]*(A[i,j]/A[i,i])

        return x

    def diag(self):
        """
        Try to convert A into a diagonally dominant matrix
        """
        row_sum = [np.sum(np.abs(self.A[i,:])) for i in range(self.n)]
        satisfies = lambda i,j: np.abs(self.A[i,j]) > row_sum[i] - np.abs(self.A[i,j])

        for i in range(self.n):
            if not satisfies(i,i):
                row = i
                for j in range(i+1,self.n):
                    if i!=j and satisfies(j,i):
                        row = j
                        break
                else:
                    for j in range(i):
                        if i!=j and satisfies(j,i) and satisfies(i,j):
                            row = j
                            break

            self.order[i],self.order[row] = self.order[row],self.order[i]
            self.A[[i,row]] = self.A[[row,i]]

        self.b = self.b[self.order]

    def norm(self, x, name='inf'):
        """
        Calculate various norms for a matrix
        Contains
        '1': max column sum
        'inf': max row sum
        '2': max value
        'frobenius': frobenius norm
        """
        name = str(name).lower()

        if name == '1':
            return max(np.sum(np.abs(x),axis=1))
        elif name == 'inf':
            return np.max(np.sum(np.abs(x),axis=0))
        elif name == '2':
            return np.max(np.abs(x))
        elif name == 'frobenius':
            return np.sqrt(np.sum(x*x))
        else:
            raise Exception(f'Norm "{name}" not implemented, choose from [1,2,inf,frobenius]')

    def stop(self, tol, norm_name):
        if self.num_iter > self.max_iter:
            return True
        if self.num_iter < 2:
            return False
        return self.norm(self.sols[-1] - self.sols[-2], norm_name) <= tol

    def jacobi(self, x0, tol, norm):
        """
        Solve using the Jacobi method
        """
        pass

    def gauss_seidel(self, x0, tol, norm):
        """
        Solve using the Gauss siedel method
        """
        mask = np.array([[i>=j for j in range(self.n)] for i in range(self.n)])
        L =  self.A*mask
        U =  self.A*(1-mask)
        L_inv = np.linalg.inv(L)

        x = x0
        x_new = x
        self.sols.append(x0)
        while not self.stop(tol, norm):
            x_new = np.dot(L_inv, self.b - np.dot(U,x))
            x = x_new
            self.sols.append(x_new)

    def find_solution(self, method, x0, tol=None, norm='inf'):
        if not tol:
            tol = self.tol

        x0 = np.array(x0)
        if x0.shape == (self.n,):
            x0 = x0.reshape(x0.shape[0],1)
        if (x0.shape == (1,self.n)):
            x0 = x0.T
        if (x0.shape != (self.n,1)):
            raise Exception(f'incorrect dimensions for x0: expected ({self.n},1) got {x0.shape}')

        if method.lower() == 'jacobi':
            self.gauss_seidel(x0,tol)
        elif method.lower() == 'gauss-seidel':
            self.gauss_seidel(x0,tol,norm)
        else:
            raise Exception(f'Method "{method}" not implemented, choose from [jacobi, gauss-seidel]')

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
        pass
