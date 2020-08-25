from flask import Flask, request, jsonify
#from flask_cors import CORS, cross_origin
from utils.zeroes import find_zeroes

app = Flask(__name__)
app.config['SECRET_KEY'] = 'The answer is 42'
#cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

def send_request(ans=[], tol=0.1, error=False, message=''):
    if not ans:
        ans = find_zeroes('0')

    return {
        'error': error, 'err_message': message,
        'f': ans.tabular_f(), 'sols': [{'x': x, 'y': ans.f(x)} for x in ans.sols],
        'sol': ans.sol,
        'tol': ans.tol,
        'num_iter': ans.num_iter,
        'ord_conv': ans.approx_convergence(),
    }

@app.route('/')
def hello():
    return "Hello! this is an API, to use the app: go to https://manansoni42.github.io/numerical_analysis/web/zeros.html"

@app.route('/zeros', methods=['POST'])
def zeros():

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
