from flask import Flask, request, jsonify, render_template, redirect
from utils.zeroes import F
from utils.lineq import Solver
from utils.interp import Points
from utils.diff import Diff_F
from utils.intg import Int_F
from utils.de import DE
from make_requests import *
import os
import warnings

warnings.filterwarnings('ignore')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'The answer is 42'

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

@app.route('/int')
def intg():
    return render_template('int.html')

@app.route('/de/ivp')
def de_ivp():
    return render_template('de-ivp.html')

@app.route('/de/bvp')
def de_bvp():
    return render_template('de-bvp.html')

@app.route('/de/ex')
def de_ex():
    return render_template('de-ex.html')

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
        fn = Diff_F(f)
    except Exception as e:
        return send_error(f'Error while initializing: {str(e)}')

    try:
        fn.differentiate(order=order, x=x0, h=h, method=method)
    except Exception as e:
        return send_error(f'Error while calculating: {str(e)}')

    return send_diff_request(fn, x0)

@app.route('/api/int', methods=['POST'])
def integrate():
    try:
        f = request.form['f']
        from_ = float(request.form['from'])
        to_ = float(request.form['to'])
        n = int(request.form['n'])
        method = request.form['method']
    except Exception as e:
        return send_error(f'Invalid input data')

    try:
        fn = Int_F(f)
    except Exception as e:
        return send_error(f'Error while initializing: {str(e)}')

    try:
        fn.integrate(from_=from_, to_=to_, num_pts=n, method=method)
    except Exception as e:
        return send_error(f'Error while calculating: {str(e)}')

    return send_intg_request(fn)

@app.route('/api/de', methods=['POST'])
def solve_de():
    try:
        type = request.form['type']
        if type == 'ivp':
            f = request.form['f']
        else:
            a,b,c = float(request.form['a']), float(request.form['b']), float(request.form['c'])

        from_ = float(request.form['from'])
        to_ = float(request.form['to'])

        try:
            h = float(request.form['h'])
        except:
            h = None
        try:
            tol = float(request.form['tol'])
        except:
            tol = None

        if type == 'ivp':
            x0 = float(request.form['x0'])
            y0 = float(request.form['y0'])
            method = request.form['method']
        else:
            b0, b1, b2 = float(request.form['b-0']), float(request.form['b-1']), float(request.form['b-2'])

        try:
            ex_num = request.form['example'].split(",")[0]
        except:
            ex_num = None

    except Exception as e:
        return send_error(f'Invalid input data')

    try:
        if type == 'ivp':
            eq = DE(f)
            eq.init_ivp(x0=x0, y0=y0)
        else:
            eq = DE([a,b,c])
            eq.init_bvp(x0=from_, xn=to_, boundary=[b0,b1,b2])
    except Exception as e:
        return send_error(f'Error while initializing: {str(e)}')

    try:
        if type == 'ivp':
            eq.solve_ivp(method=method, interval=(from_, to_), h=h, tol=tol)
        else:
            eq.solve_bvp(h=h)
    except Exception as e:
        return send_error(f'Error while calculating: {str(e)}')

    return send_de_request(eq, ex_num)
#####################################

if __name__ == '__main__':
    app.run(debug=True)
