from flask import Flask, render_template, request, redirect, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from tax_app import TaxApp
from werkzeug.urls import url_quote  # Updated import

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
Bootstrap(app)
tax_app = TaxApp()

class LoginForm(FlaskForm):
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    submit = SubmitField('View Account')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        phone_number = form.phone_number.data
        # Use werkzeug.urls.url_quote instead of url_encode
        return redirect(f'/account/{url_quote(phone_number)}')
    return render_template('index.html', form=form)

@app.route('/account/<phone_number>')
def account(phone_number):
    try:
        # Get account information
        status = tax_app.check_status(phone_number)
        tax_code = tax_app.check_tax_code(phone_number)
        
        # Get yearly returns
        years = [2023, 2022, 2021]  # Example years
        returns = {}
        for year in years:
            returns[year] = tax_app.check_tax_return(phone_number, year)
        
        return render_template('account.html', 
                             phone_number=phone_number,
                             status=status,
                             tax_code=tax_code,
                             returns=returns)
    except Exception as e:
        flash(str(e))
        return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) 