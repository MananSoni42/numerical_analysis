from utils.zeroes import F
from utils.lineq import Solver
from utils.interp import Points
import numpy as np

def send_error(message):
    return {
        'error': True,
        'err_message': message
    }

def send_zero_request(ans):
    return {
        'error': False,
        'f': ans.tabular_f(), 'sols': [{'n': n+1, 'x': x, 'y': ans.f(x)} for n,x in enumerate(ans.sols)],
        'num_f': [{'x': n+1, 'y': x, 'n': n+1} for n,x in enumerate(ans.sols)],
        'sol': round(ans.sol, 5),
        'tol': ans.tol,
        'num_iter': ans.num_iter,
        'ord_conv': max(0, ans.approx_convergence()),
    }

def send_lineq_request(ans):
    return {
        'error': False,
        'cond': ans.cond_num(),
        'diag': int(ans.is_diag(ans.A_orig)),
        'diag_transform': int(ans.is_diag(ans.A)),
        'A_diag': ans.A.tolist(),
        'sol': ans.sol.tolist(),
        'tol': ans.tol,
        'num_iter': ans.num_iter,
    }

def send_interp_request(poly):
    x,y = poly.table()
    return {
        'error': False,
        'simple': [round(val,3) for val in poly.sol],
        'lagrange': [round(val,3) for val in poly.lagrange_coeffs],
        'newton': [round(val,3) for val in poly.newton_coeffs],
        'poly': [{ 'x': x[i], 'y': y[i] } for i in range(len(x))],
        'data': [{'x': poly.x[i], 'y': poly.fx[i]} for i in range(len(poly.x))]
    }

def send_diff_request(fn, x0):
    x,y,y_ = fn.table(range=(x0-10, x0+10))
    return {
        'error': False,
        'f': [{'x': x[i], 'y': round(y[i],3)} for i in range(len(x))],
        'f_': [{'x': x[i], 'y': round(y_[i],3)} for i in range(len(x))],
        'x0': [{'x': x0, 'y': fn.differentiate(order=fn.n, x=x0, h=fn.h, method=fn.method) }],
        'y_min': min(y),
        'y_max': max(y)
    }

def send_intg_request(fn):
    x,y = fn.table()
    return {
        'error': False,
        'ans': round(fn.sol,5),
        'f': [{'x': x[i], 'y': round(y[i],3)} for i in range(len(x))],
        'pts': [{'x': pt, 'y': y} for pt in fn.int_pts for y in np.linspace(0,fn.f(pt),100) ]
    }
