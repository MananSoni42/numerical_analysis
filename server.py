from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS
from utils.zeroes import find_zeroes
import warnings

warnings.filterwarnings('ignore')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'The answer is 42'
CORS(app)

def send_request(ans=[], tol=0.1, error=False, message=''):
    if not ans:
        ans = find_zeroes('0')

    return {
        'error': error, 'err_message': message,
        'f': ans.tabular_f(), 'sols': [{'n': n+1, 'x': x, 'y': ans.f(x)} for n,x in enumerate(ans.sols)],
        'num_f': [{'x': n+1, 'y': x, 'n': n+1} for n,x in enumerate(ans.sols)],
        'sol': round(ans.sol, 5),
        'tol': ans.tol,
        'num_iter': ans.num_iter,
        'ord_conv': max(0, ans.approx_convergence()),
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/zeroes')
def zeroes():
    return render_template('zeroes.html')

@app.route('/api/zeroes', methods=['POST'])
def find_zeros():

    try:
        f = request.form['f']
        method = request.form['method']
        tol = min(0.1, float(request.form['tol']))
        initial = [float(val) for val in request.form['initial'].replace('(','').replace(')','').split(',')]
        stopmethod = request.form['stop']
    except Exception as e:
        return send_request(error=True, message=f'Invalid form inputs: {str(e)}')

    try:
        ans = find_zeroes(f)
    except Exception as e:
        return send_request(error=True, message=f'Could not parse f(x): {str(e)}')

    try:
        ans.find(method=method, initial=initial, tol=tol, stopmethod=stopmethod)
    except Exception as e:
        return send_request(error=True, message=f'Error while finding zeroes: {str(e)}')

    return send_request(ans)

if __name__ == '__main__':
    app.run()
