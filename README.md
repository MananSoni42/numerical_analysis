
# Numerical Analysis
This repository contains visualizations for the course Numerical Analysis (MATH F313) at BITS Pilani. The aim of this Repository is to provide useful visualizations so that students (like me!) can better understand the course material.

> This content can also be accessed on the web. Visit [na-bits.herokuapp.com](http://na-bits.herokuapp.com/) for the interactive version.

## Usage
### 1. Finding zeroes
Use this module to find zeroes for any function you like!  
- Initialize ```F``` with a valid function f(x)
- Find zeroes of f(x) using ```F.find_zeroes()```. Solutions can be found using a variety of methods
- Visualize the solution using ```F.visualize()```
- A working example is provdided in ```example-find-zeroes.py```

####  Parameters:
- **initial** (string): comma seperated list of values for the initial parameters
- **method** (string):  one of ["bisection", "regula-falsi", "secant", "newton"]
- **tol** (float):  acceptable tolerance level
- **stopmode** (string):  one of ["abs", "rel", "func"]
	Stopping criterion for any method
	- **"abs":**  Use absolute error to terminate i.e terminate when:
            |x_{n} - x_{n-1}| < tol
    - **"rel":** Use relative error to terminate i.e terminate when:
            |x_{n} - x_{n-1}| / | x_{n-1} | < tol
    - **"func":** Use the given function to terminate i.e terminate when:
            | f(x_{n}) | < tol

### 2. Solving linear equations
Use this module to solve arbitrarily large linear equations numerically!  
- The equations are represented by Ax = b
- Initialize the ```Solver``` with A and b
- Find solutions using ```Solver.find_solution()```.
- A working example is provdided in ```example-solve-lineq.py```

####  Parameters:
- **method** (string):  one of ["exact", "gauss-elim", "jacobi", "gauss-seidel"]
- **x0** (list): Initial solution estimate (dimensions must be same as that of b)
- **tol** (float):  acceptable tolerance level
- **norm** (string):  one of ["1", "2", "inf", "frobenius"]
	Matrix norm to be used
	- **"1":** Maximum over the row sum of absolute values
	- **"inf":** Maximum over the column sum of absolute values
	- **"2":** Maximum absolute value in the entire matrix
	- **"frobenius":** sqrt of (Sum of square of all values in the matrix)

### 3. Polynomial interpolation
Use this module to interpolate from an existing table of data using polynomials of appropriate degree
- Provide a list of values for x, y and optionally for y'
- Initialize ```Points``` with x, y (and y' optionally)
- Interpolate using ```Points.interpolate()```.
- You can also visualize using ```Points.visualize()```.
- A working example is provdided in ```example-interpolate.py```

####  Parameters:
- **method** (string):  one of ["lagrange", "newton", "hermite"]

## Installing locally
This project requires python (3.7+)
1. Install [Python](https://www.python.org/) and [pip](https://pip.pypa.io/en/stable/)
2. Install the required dependancies using pip  
 ```
pip install -r requirements.txt
 ```
3.  Use the classes provided in the ```utils``` directory.

## Contributing
Feel free to contribute features / point out errors. Fork this repository and make a pull request.  

## License
This project is licensed under the [MIT](https://opensource.org/licenses/MIT) License
