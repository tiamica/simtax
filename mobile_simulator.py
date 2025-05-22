import requests
from datetime import datetime

MOCK_SERVER_URL = 'http://localhost:5000'

def check_server_connection():
    try:
        response = requests.get(f'{MOCK_SERVER_URL}/', timeout=5)
        return response.status_code == 200
    except:
        return False

def handle_tax_command(phone_number, year=None):
    if not check_server_connection():
        return "Error: Could not connect to the server. Please ensure the mock server is running."
    
    try:
        response = requests.post(
            f'{MOCK_SERVER_URL}/tax/{phone_number}',
            json={'year': year},
            timeout=5
        )
        if response.status_code != 200:
            raise Exception(response.json().get('error', 'Failed to calculate tax'))
        
        tax_data = response.json()['data']
        return (f"Tax calculation for {tax_data['year']}:\n"
                f"Income: ₦{tax_data['income']:,.2f}\n"
                f"Expenses: ₦{tax_data['expenses']:,.2f}\n"
                f"Taxable Income: ₦{tax_data['taxable_income']:,.2f}\n"
                f"Tax Owed: ₦{tax_data['tax_owed']:,.2f}")
    except Exception as e:
        return f"Error calculating tax: {str(e)}"

def handle_return_command(phone_number, year=None):
    if not check_server_connection():
        return "Error: Could not connect to the server. Please ensure the mock server is running."
    
    try:
        response = requests.post(
            f'{MOCK_SERVER_URL}/return/{phone_number}',
            json={'year': year},
            timeout=5
        )
        if response.status_code != 200:
            raise Exception(response.json().get('error', 'Failed to check return'))
        
        return_data = response.json()['data']
        return (f"Tax return for {return_data['year']}:\n"
                f"Income: ₦{return_data['income']:,.2f}\n"
                f"Expenses: ₦{return_data['expenses']:,.2f}\n"
                f"Tax Paid: ₦{return_data['tax_paid']:,.2f}\n"
                f"Status: {return_data['status']}")
    except Exception as e:
        return f"Error checking return: {str(e)}" 