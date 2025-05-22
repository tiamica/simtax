from flask import Flask, render_template, request, redirect, flash, jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.urls import url_quote
import requests
import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
Bootstrap(app)

# Mock server URL
MOCK_SERVER_URL = 'http://localhost:5000'

class LoginForm(FlaskForm):
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    submit = SubmitField('View Account')

def get_user_status(phone_number):
    try:
        response = requests.get(f'{MOCK_SERVER_URL}/status/{phone_number}')
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException:
        return None

def get_user_tax_return(phone_number, year):
    try:
        response = requests.get(f'{MOCK_SERVER_URL}/status/{phone_number}/{year}')
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        phone_number = form.phone_number.data
        return redirect(f'/account/{url_quote(phone_number)}')
    return render_template('index.html', form=form)

@app.route('/account/<phone_number>')
def account(phone_number):
    try:
        # Get account information from mock server
        status_data = get_user_status(phone_number)
        if not status_data:
            flash('User not found')
            return redirect('/')

        # Get yearly returns
        current_year = datetime.datetime.now().year
        years = range(2019, current_year + 2)
        returns = {}
        
        for year in years:
            return_data = get_user_tax_return(phone_number, year)
            if return_data:
                returns[year] = {
                    'income': return_data.get('income', 0),
                    'expenses': return_data.get('expenses', 0),
                    'tax_paid': return_data.get('tax_paid', 0)
                }
            else:
                returns[year] = {
                    'income': 0,
                    'expenses': 0,
                    'tax_paid': 0
                }

        return render_template('account.html', 
                            phone_number=phone_number,
                            status=status_data.get('status', 'No status available'),
                            tax_code=status_data.get('tax_code', 'N/A'),
                            returns=returns)
    except Exception as e:
        flash(str(e))
        return redirect('/')

@app.route('/calculate-tax/<phone_number>', methods=['POST'])
def calculate_tax(phone_number):
    try:
        year = request.json.get('year', datetime.now().year)
        response = requests.post(
            f'{MOCK_SERVER_URL}/tax/{phone_number}',
            json={'year': year}
        )
        if response.status_code != 200:
            raise Exception(response.json().get('error', 'Failed to calculate tax'))
        
        tax_data = response.json()['data']
        return render_template('tax_calculation.html',
                             phone_number=phone_number,
                             year=year,
                             tax_data=tax_data)
    except Exception as e:
        flash(str(e))
        return redirect(f'/account/{phone_number}')

@app.route('/check-return/<phone_number>', methods=['POST'])
def check_return(phone_number):
    try:
        year = request.json.get('year', datetime.now().year)
        response = requests.post(
            f'{MOCK_SERVER_URL}/return/{phone_number}',
            json={'year': year}
        )
        if response.status_code != 200:
            raise Exception(response.json().get('error', 'Failed to check return'))
        
        return_data = response.json()['data']
        return render_template('return_info.html',
                             phone_number=phone_number,
                             year=year,
                             return_data=return_data)
    except Exception as e:
        flash(str(e))
        return redirect(f'/account/{phone_number}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) 