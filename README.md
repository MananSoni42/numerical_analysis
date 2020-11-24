# Numerical Analysis
This repository contains visualizations for the course Numerical Analysis (MATH F313) at BITS Pilani. The aim of this Repository is to provide useful visualizations so that students (like me!) can better understand the course material.

> **Production branch**  
> This branch **automatically** deploys to [na-bits.herokuapp.com](http://na-bits.herokuapp.com/) using Heroku when a new commit is pushed  
> Ensure that the code runs (currently, no tests are configured)

## Table of contents

* [Usage](#usage)
* [1. Finding zeroes](#1-finding-zeroes)
* [2. Solving linear equations](#2-solving-linear-equations)
* [3. Polynomial interpolation](#3-polynomial-interpolation)
* [4. Numerical Differentiation](#4-numerical-differentiation)
* [5. Numerical Integration](#5-numerical-integration)
* [6. Solving Differential Equations](#6-solving-differential-equations)
* [Installing locally](#installing-locally)
* [Contributing](#contributing)
* [License](#license)

## Usage

All the libraries have a uniform calling style:
* Instantiate the class (```C```)
* Perform calculation using the given method (```method()```)
* Answer is available in ```C.sol```
* Visualize the answer using ```C.visualize()```
* An example for each module is given files: ```example-<module>-<name>.py```

| Module | Class ```C```   | ```method()```          |
|--------|-----------------|-------------------------|
| 1      | F               | find_zeroes()            |
| 2      | Solver          | find_solution()          |
| 3      | Points          | interpolate()           |
| 4      | Diff_F           | differentiate()          |
| 5      | Int_F           | integrate()             |
| 6      | DE (IVP)        | init_ivp(), solve_ivp() |
| 6      | DE (BVP)        | init_bvp(), solve_bvp() |

## 1. Finding zeroes
- Use this module to find zeroes for any function you like!
- visualizations available
- A working example is provdided in ```example-1-find-zeroes.py```

### Parameters:
- **initial** (string): comma seperated list of values for the initial parameters
- **method** (string):  one of ["bisection", "regula-falsi", "secant", "newton"]
- **tol** (float):  acceptable tolerance level
- **stopmode** (string):  one of ["abs", "rel", "func"]
	Stopping criterion for any method
	- **"abs":**  Use absolute error to terminate i.e terminate when:
	    <img src="https://render.githubusercontent.com/render/math?math=| x_{n} - x_{n-1} | < tol">
    - **"rel":** Use relative error to terminate i.e terminate when:
	    <img src="https://render.githubusercontent.com/render/math?math=| \frac{x_{n} - x_{n-1}}{x_{n-1}} | < tol">
    - **"func":** Use the given function to terminate i.e terminate when:
	    <img src="https://render.githubusercontent.com/render/math?math=| f(x_{n}) | < tol">

## 2. Solving linear equations
- Use this module to solve arbitrarily large linear equations numerically!
- visualizations not available
- A working example is provdided in ```example-2-solve-lineq.py```

### Parameters:
- **method** (string):  one of ["exact", "gauss-elim", "jacobi", "gauss-seidel"]
- **x0** (list): Initial solution estimate (dimensions must be same as that of b)
- **tol** (float):  acceptable tolerance level
- **norm** (string):  one of ["1", "2", "inf", "frobenius"]
	Matrix norm to be used
	- **"1":** Maximum over the row sum of absolute values
	- **"inf":** Maximum over the column sum of absolute values
	- **"2":** Maximum absolute value in the entire matrix
	- **"frobenius":** sqrt of the squared sum of all values in the matrix

## 3. Polynomial interpolation
- Use this module to interpolate from an existing table of data using polynomials
- visualizations available
- A working example is provdided in ```example-3-interpolate.py```

### Parameters:
- None

## 4. Numerical Differentiation
- Use this module to numerically differentiate a given function
- visualizations available
- A working example is provdided in ```example-4-differentiate.py```

### Parameters:
- **method** (string):  one of ["forward", "central", "backward"]
- **x** (float): Point at which to differentiate
- **order** (int): Order of differentiation (how many times to differentiate)
- **h** (float): change in x (approximation of the limit definition)

## 5. Numerical Integration
- Use this module to numerically integrate a given function
- visualizations available
- A working example is provdided in ```example-5-integrate.py```

### Parameters:
- **method** (string):  one of ["trap", "simp", "simp_3/8", "gauss_legendre"]
    Method to use
    - **"trap":** Use the trapezoid rule
    - **"simp":** Use Simpson's rule (requires **2k+1** points)
    - **"simp":** Use Simpson's 3/8 rule (requires **3k+1** points)
    - **"gauss_legendre":** Use the Gauss Legendre method
- **from_** (float): Point from which to integrate
- **to_** (float): Point till which to integrate
- **num_pts** (string): number of points to use (between ```from_``` and ```to_```)

## 6. Solving Differential Equations
- Use this module to solve first order Differential equations
- visualizations available
- A working example is provdided in ```example-6-diff-eq.py```

### 6.1 Initial Value Problems
- solve any first order Initial Value problems
- The initial conditions need to be specified using the ```init_ivp()``` method
- It is solved using the ```solve_ivp()``` method
- A working example is provdided in ```example-6-diff-eq-ivp.py```

#### Parameters:
- **method** (string):  one of ['euler', 'modified-euler', 'adaptive-euler', 'runge-kutta-4', 'adam-bashforth-2', 'adam-bashforth-3', 'adam-bashforth-4', 'adam-bashforth-pc', 'milne-pc', 'adam-milne-pc']
    Method to use for numerical solutions
	- Single step methods:
		- **"euler":** Euler's method (equivalent to a first order Taylor series approximation)
		- **"modified-euler":** Modified euler's method (equivalent to Runge Kutta of order 2)
		- **"runge-kutta-4":** 4th order Runge Kutta method (the best single step method of those implemented)
		- **"adaptive-euler":** An adaptive version of Modified euler's method that sets the step size `h` automatically according to the specified tolerance (`tol` parameter)
		> **NOTE**: The tolerance parameter indicates the local truncation error

	- multi step methods (explicit):
		- **"adam-bashforth-2":** 2nd order adam-bashforth method (Uses a 1st order polynomial for approximations)
		- **"adam-bashforth-3":** 3nd order adam-bashforth method (Uses a 2st order polynomial for approximations)
		- **"adam-bashforth-4":** 4nd order adam-bashforth method (Uses a 3rd order polynomial for approximations)
	> **NOTE**: All initial points required for the polynomials are approximated using Euler's method

	- Predictor corrector methods:
		- **"adam-bashforth-pc":** Uses 4th order adam-bashforth polynomials for the predictor and corrector
		- **"milne-pc":** Uses 4th order milne polynomials for the predictor and corrector
		- **"adam-bashforth-pc":** Uses 4th order adam-bashforth polynomials for the predictor and corrector, applies the predictor repeatedly till convergence (requires a `tol` parameter)
		> **NOTE**: The tolerance parameter indicates the convergence criterion for the predictor equation

- **h** (float): Step size to use
- **tols** (float): A tolerance parameter, only used in `adaptive-euler` and `adam-milne-pc`
- **interval** (tuple): The interval in which to solve
> **NOTE**: The left endpoint of the interval must be same as x0 ( from the initial condition )

### 6.2 Boundary Value Problems
- solve any *linear* first order Boundary Value problem
- The initial conditions need to be specified using the ```init_bvp()``` method
- It is solved using the ```solve_bvp()``` method
- A working example is provdided in ```example-6-diff-eq-bvp.py```

#### Parameters:
- None

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
