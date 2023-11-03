from flask import Flask, render_template, request, flash, redirect, url_for
from currency import get_currency_conversion

app = Flask(__name__)
app.secret_key = 'secret-key'

@app.route('/', methods=['GET', 'POST'])
def index():
    options = []
    with open('options.txt') as f:
        for line in f:
            option_value = line.split()[0]
            options.append(option_value)
    if request.method == 'POST':
        from_currency = request.form.get('from_currency')
        to_currency = request.form.get('to_currency')
        amount = request.form.get('amount')
        if not from_currency or not to_currency or not amount:
            flash('Please fill out all the fields.')
            return redirect(url_for('index'))
        result = get_currency_conversion(from_currency, to_currency, amount)
        if result is not None:
            return render_template('index.html', result=result, options=options, from_currency=from_currency, to_currency=to_currency, amount=amount), 200
        else:
            result = "Error: The API response does not contain a 'result' key."
            return render_template('error.html', error_message=result)
    return render_template('index.html', options=options)


@app.errorhandler(400)
def bad_request(error):
    return render_template('error.html', error_message='400 Bad Request'), 400

@app.errorhandler(401)
def unauthorized(error):
    return render_template('error.html', error_message='401 Unauthorized'), 401

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error_message='404 Page Not Found'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', error_message='500 Internal Server Error'), 500

if __name__ == '__main__':
    app.run(debug=True)