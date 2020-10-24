from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS
from utils.zeroes import F
from utils.lineq import Solver
from utils.interp import Points
from utils.diff import Diff_Fn
from make_requests import *
import os
import warnings

warnings.filterwarnings('ignore')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'The answer is 42'
CORS(app)

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

@app.route('/diff')
def diff():
    return render_template('diff.html')

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
        return send_error(f'Invalid input data')

    try:
        ans = F(func)
    except Exception as e:
        return send_error(f'Error while initializing: {str(e)}')

    try:
        ans.find_zeroes(method=method, initial=initial, tol=tol, stopmethod=stopmethod)
    except Exception as e:
        return send_error(f'Error while calculating: {str(e)}')

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
        return send_error(f'Invalid input data')

    try:
        lineq = Solver(A,b)
    except Exception as e:
        return send_error(f'Error while initializing: {str(e)}')

    try:
        lineq.find_solution(method=method, x0=x0,tol=tol,norm=norm)
    except Exception as e:
        return send_error(f'Error while calculating: {str(e)}')

    return send_lineq_request(lineq)

@app.route('/api/interp', methods=['POST'])
def interpolate():
    try:
        n = int(request.form['n'])
        x = [float(request.form[f'{i}-{0}']) for i in range(n)]
        y = [float(request.form[f'{i}-{1}']) for i in range(n)]
        y_ = [float(request.form[f'{i}-{2}']) if request.form[f'{i}-{2}'] else float('nan') for i in range(n)]
    except Exception as e:
        return send_error(f'Invalid input data')

    try:
        pts = Points(x,y,y_)
    except Exception as e:
        return send_error(f'Error while initializing: {str(e)}')

    try:
        pts.interpolate()
    except Exception as e:
        return send_error(f'Error while calculating: {str(e)}')

    return send_interp_request(pts)

@app.route('/api/diff', methods=['POST'])
def differentiate():
    try:
        f = request.form['f']
        x0 = float(request.form['x0'])
        h = float(request.form['h'])
        method = request.form['method']
        order = int(request.form['order'])
    except Exception as e:
        return send_error(f'Invalid input data')

    try:
        fn = Diff_Fn(f)
    except Exception as e:
        return send_error(f'Error while initializing: {str(e)}')

    try:
        fn.diff(order=order, x=x0, h=h, method=method)
    except Exception as e:
        return send_error(f'Error while calculating: {str(e)}')

    return send_diff_request(fn, x0)


#####################################

if __name__ == '__main__':
    app.run()
