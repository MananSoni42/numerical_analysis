from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS
from utils.zeroes import F
from utils.lineq import Solver
import os
import warnings

warnings.filterwarnings('ignore')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'The answer is 42'
CORS(app)

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

## Serve the frontend pages ##

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/zeroes')
def zeroes():
    return render_template('zeroes.html')

@app.route('/lineq')
def lineq():
    return render_template('lineq.html')

@app.route('/interp')
def interp():
    return render_template('interp.html')

##############################

###### backend APIs used ######

@app.route('/api/zeroes', methods=['POST'])
def find_zeros():

    try:
        func = request.form['f']
        method = request.form['method']
        tol = min(0.1, float(request.form['tol']))
        initial = [float(val) for val in request.form['initial'].replace('(','').replace(')','').split(',')]
        stopmethod = request.form['stop']
    except Exception as e:
        return send_zero_request(error=True, message=f'Invalid form inputs: {str(e)}')

    try:
        ans = F(func)
    except Exception as e:
        return send_zero_request(error=True, message=f'Could not parse f(x): {str(e)}')

    try:
        ans.find_zeroes(method=method, initial=initial, tol=tol, stopmethod=stopmethod)
    except Exception as e:
        return send_zero_request(error=True, message=f'Error while finding zeroes: {str(e)}')

    return send_zero_request(ans)

@app.route('/api/lineq', methods=['POST'])
def solve_lineq():
    try:
        n = int(request.form['n'])
        A = [[float(request.form[f'{i}-{j}']) for j in range(n)] for i in range(n)]
        b = [float(request.form[f'{i}-{n}']) for i in range(n)]
    except Exception as e:
        return send_lineq_request(error=True, message=f'Invalid Matrix inputs')

    try:
        method = request.form['method']
        tol = min(0.1,float(request.form['tol']))
        norm = request.form['norm']
        x0 = [float(val) for val in request.form['initial'].split(',')]
    except Exception as e:
        return send_lineq_request(error=True, message=f'Invalid option: {str(e)}')

    try:
        lineq = Solver(A,b)
    except Exception as e:
        return send_lineq_request(error=True, message=f'Error while initializing matrices: {str(e)}')

    try:
        lineq.find_solution(method=method, x0=x0,tol=tol,norm=norm)
    except Exception as e:
        return send_lineq_request(error=True, message=f'Error while finding solution: {str(e)}')

    return send_lineq_request(lineq)

#####################################

if __name__ == '__main__':
    extra_dirs = ['.',]
    extra_files = extra_dirs[:]
    for extra_dir in extra_dirs:
        for dirname, dirs, files in os.walk(extra_dir):
            for filename in files:
                filename = os.path.join(dirname, filename)
                if os.path.isfile(filename):
                    extra_files.append(filename)
    app.run(debug=True, extra_files=extra_files)
