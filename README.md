
# Numerical Analysis
This repository contains visualizations for the course Numerical Analysis (MATH F313) at BITS Pilani. The aim of this Repository is to provide useful visualizations so that students (like me!) can better understand the course material.

> The contents of this repository can be accessed in 2 ways:
> 1. An interactive website (with limited functionality): [na-bits.herokuapp.com](http://na-bits.herokuapp.com/)
> 2. A Python API (with complete functionality): This repository

## Table of contents

* [Usage](#usage)
* [1. Finding zeroes](#1-finding-zeroes)
* [2. Solving linear equations](#2-solving-linear-equations)
* [3. Polynomial interpolation](#3-polynomial-interpolation)
* [4. Numerical Differentiation](#4-numerical-differentiation)
* [5. Numerical Integration](#5-numerical-integration)
* [Installing locally](#installing-locally)
* [Contributing](#contributing)
* [License](#license)

## Usage

All the libraries have a uniform calling style:
* Instantiate the class (```C```)
* Perform calculation using the given method (```method()```)
* Answer is available in ```C.sol```
* Visualize the answer using ```C.visualize()```

| Module | Class ```C```   | ```method()```   |
|--------|-----------------|------------------|
| 1      | F               | find_zeroes()     |
| 2      | Solver          | find_solution()   |
| 3      | Points          | interpolate()    |
| 4      | Diff_F           | differentiate()   |
| 5      | Int_F           | integrate()      |

## 1. Finding zeroes
- Use this module to find zeroes for any function you like!
- visualizations available
- A working example is provdided in ```example-find-zeroes.py```

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
- A working example is provdided in ```example-solve-lineq.py```

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
- A working example is provdided in ```example-interpolate.py```

### Parameters:
- None

## 4. Numerical Differentiation
- Use this module to numerically differentiate a given function
- visualizations available
- A working example is provdided in ```example-differentiate.py```

### Parameters:
- **method** (string):  one of ["forward", "central", "backward"]
- **x** (float): Point at which to differentiate
- **order** (int): Order of differentiation (how many times to differentiate)
- **h** (float): change in x (approximation of the limit definition)

## 5. Numerical Integration
- Use this module to numerically integrate a given function
- visualizations available
- A working example is provdided in ```example-integrate.py```

### Parameters:
- **method** (string):  one of ["trap", "simp", "simp_3/8", "gauss_legendre"]
    Method to use
    - **"trap":** Use the trapezoid rule
    - **"simp":** Use Simpson's rule (requires 2k+1 points)
    - **"simp":** Use Simpson's 3/8 rule (requires 3k+1 points)
    - **"gauss_legendre":** Use the Gauss Legendre method
- **from_** (float): Point from which to integrate
- **to_** (float): Point till which to integrate
- **num_pts** (string): number of points to use (between ```from_``` and ```to_```)

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
