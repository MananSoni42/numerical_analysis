from utils.zeroes import F
from utils.lineq import Solver
from utils.interp import Points

def send_zero_request(ans=[], error=False, message=''):
    if not ans:
        ans = F('0')

    return {
        'error': error, 'err_message': message,
        'f': ans.tabular_f(), 'sols': [{'n': n+1, 'x': x, 'y': ans.f(x)} for n,x in enumerate(ans.sols)],
        'num_f': [{'x': n+1, 'y': x, 'n': n+1} for n,x in enumerate(ans.sols)],
        'sol': round(ans.sol, 5),
        'tol': ans.tol,
        'num_iter': ans.num_iter,
        'ord_conv': max(0, ans.approx_convergence()),
    }

def send_lineq_request(ans=[], error=False, message=''):
    if not ans:
        ans = Solver([[1]],[1])
        ans.find_solution('exact',[0])

    return {
        'error': error, 'err_message': message,
        'cond': ans.cond_num(),
        'diag': int(ans.is_diag(ans.A_orig)),
        'diag_transform': int(ans.is_diag(ans.A)),
        'A_diag': ans.A.tolist(),
        'sol': ans.sol.tolist(),
        'tol': ans.tol,
        'num_iter': ans.num_iter,
    }

def send_interp_request(poly=None, error=False, message=''):
    if not poly:
        poly = Points([[0]],[0])
        poly.interpolate(method='lagrange')

    x,y = poly.table()
    print(poly.x, poly.fx)
    return {
        'method': poly.method,
        'error': error, 'err_message': message,
        'var': 'P' if poly.method == 'lagrange' else 'N',
        'unsimple': [round(val,3) for val in poly.coeffs],
        'simple': [round(val,3) for val in poly.sol],
        'poly': [{ 'x': x[i], 'y': y[i] } for i in range(len(x))],
        'data': [{'x': poly.x[i], 'y': poly.fx[i]} for i in range(len(poly.x))]
    }
