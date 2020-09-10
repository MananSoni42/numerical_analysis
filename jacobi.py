def jacobi(self, x0, tol, norm):
        """
        Solve using the Jacobi method
        """
        D = np.diag(np.diag(self.A))
        LU = self.A - D
        
        x = x0
        x_new = x
        self.sols.append(x0)

        while not self.stop(tol, norm):
            D_inv = np.diag(1 / np.diag(D))
            x_new = np.dot(D_inv, self.b - np.dot(LU, x))
            x = x_new
            self.sols.append(x_new)