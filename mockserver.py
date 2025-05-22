from flask import Flask, request, jsonify
from tax_app import TaxApp
import threading
import time
from flask_cors import CORS
from datetime import datetime
import csv
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
tax_app = TaxApp()

CSV_FILE = 'data/tax_data.csv'

# Nigerian Personal Income Tax Rates (2023)
TAX_RATES = [
    (300000, 0.07),    # First 300,000 at 7%
    (300000, 0.11),    # Next 300,000 at 11%
    (500000, 0.15),    # Next 500,000 at 15%
    (500000, 0.19),    # Next 500,000 at 19%
    (1600000, 0.21),   # Next 1,600,000 at 21%
    (3200000, 0.24)    # Above 3,200,000 at 24%
]

def read_csv():
    if not os.path.exists('data'):
        os.makedirs('data')
    
    if not os.path.exists(CSV_FILE):
        # Create file with headers if it doesn't exist
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['phone_number', 'tin', 'tax_year', 'income', 'expenditure', 'status', 'tax_code', 'tax_paid'])
            writer.writeheader()
        return []
    
    with open(CSV_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        return list(reader)

def write_csv(data):
    fieldnames = ['phone_number', 'tin', 'tax_year', 'income', 'expenditure', 'status', 'tax_code', 'tax_paid']
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def get_user_data(phone_number):
    records = read_csv()
    return [record for record in records if record['phone_number'] == phone_number]

def update_user_record(phone_number, year, updates):
    records = read_csv()
    record_updated = False
    
    # Find and update existing record
    for record in records:
        if record['phone_number'] == phone_number and record['tax_year'] == str(year):
            # Ensure all required fields exist
            for field in ['income', 'expenditure', 'tax_paid']:
                if field not in record:
                    record[field] = '0'
            record.update(updates)
            record_updated = True
            break
    
    # Create new record if none exists
    if not record_updated:
        new_record = {
            'phone_number': phone_number,
            'tax_year': str(year),
            'income': '0',
            'expenditure': '0',
            'status': 'pending',
            'tax_code': f"TAX-{phone_number[-6:]}",
            'tax_paid': '0',
            'tin': ''
        }
        new_record.update(updates)
        records.append(new_record)
    
    write_csv(records)
    return True

def calculate_nigeria_tax(taxable_income):
    """Calculate tax based on Nigerian personal income tax rates"""
    tax = 0
    remaining_income = taxable_income
    
    for threshold, rate in TAX_RATES:
        if remaining_income <= 0:
            break
        amount = min(threshold, remaining_income)
        tax += amount * rate
        remaining_income -= amount
    
    # Apply 24% for any amount above the last threshold
    if remaining_income > 0:
        tax += remaining_income * 0.24
    
    return tax

# Simulate shortcode provider
class MockShortcodeProvider:
    def __init__(self):
        self.messages = []
        self.running = False

    def start(self):
        self.running = True
        threading.Thread(target=self.process_messages).start()

    def stop(self):
        self.running = False

    def receive_message(self, phone_number, message):
        self.messages.append({
            'phone_number': phone_number,
            'message': message,
            'timestamp': time.time()
        })

    def process_messages(self):
        while self.running:
            if self.messages:
                message = self.messages.pop(0)
                response = tax_app.process_message(
                    message['phone_number'], 
                    message['message']
                )
                print(f"Response to {message['phone_number']}: {response}")
            time.sleep(1)

# API Endpoints
@app.route('/send', methods=['POST'])
def receive_message():
    data = request.json
    phone_number = data['phone_number']
    message = data['message']
    
    # Process message and return the response
    response = process_message(phone_number, message)
    return response

def process_message(phone_number, message):
    parts = message.upper().split()
    command = parts[0]
    current_year = datetime.now().year
    
    try:
        if command == "REG":
            tin = parts[1]
            # Create initial record for registration
            new_record = {
                'phone_number': phone_number,
                'tin': tin,
                'tax_year': str(current_year),
                'income': '0',
                'expenditure': '0',
                'status': 'active',
                'tax_code': f"TAX-{tin[-6:]}",
                'tax_paid': '0'
            }
            
            # Read existing records
            records = read_csv()
            
            # Check if user already exists for current year
            existing_record = next((r for r in records if r['phone_number'] == phone_number and r['tax_year'] == str(current_year)), None)
            
            if existing_record:
                existing_record.update(new_record)
            else:
                records.append(new_record)
            
            write_csv(records)
            return jsonify({'status': 'success', 'message': f'Registered with TIN: {tin}'})
            
        elif command in ["INC", "EXP"]:
            amount = float(parts[1])
            year = current_year if len(parts) < 3 else int(parts[2])
            
            # Read existing records
            records = read_csv()
            
            # Find user's record for the specified year
            record_index = next((i for i, r in enumerate(records) 
                               if r['phone_number'] == phone_number and r['tax_year'] == str(year)), None)
            
            if record_index is not None:
                # Update existing record
                if command == "INC":
                    current_amount = float(records[record_index].get('income', '0'))
                    records[record_index]['income'] = str(current_amount + amount)
                else:  # EXP
                    current_amount = float(records[record_index].get('expenditure', '0'))
                    records[record_index]['expenditure'] = str(current_amount + amount)
            else:
                # Create new record for the year
                new_record = {
                    'phone_number': phone_number,
                    'tin': '',
                    'tax_year': str(year),
                    'income': '0',
                    'expenditure': '0',
                    'status': 'pending',
                    'tax_code': f"TAX-{phone_number[-6:]}",
                    'tax_paid': '0'
                }
                
                if command == "INC":
                    new_record['income'] = str(amount)
                else:  # EXP
                    new_record['expenditure'] = str(amount)
                
                records.append(new_record)
            
            write_csv(records)
            return jsonify({
                'status': 'success',
                'message': f'Updated {command.lower()} for year {year}'
            })
            
        elif command == "PAY":
            if len(parts) < 2:
                return jsonify({'error': 'Payment amount required'}), 400
                
            amount = float(parts[1])
            year = current_year if len(parts) < 3 else int(parts[2])
            
            # Call the payment endpoint
            response = handle_tax_payment(phone_number, amount, year)
            if response.status_code == 200:
                data = response.get_json()
                return jsonify({
                    'status': 'success',
                    'message': f'Payment of ₦{amount:,.2f} processed. Remaining tax: ₦{data["data"]["remaining_tax"]:,.2f}'
                })
            else:
                return response
            
        else:
            return jsonify({'error': 'Invalid command'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/status/<phone_number>', methods=['GET'])
def get_status(phone_number):
    user_data = get_user_data(phone_number)
    if not user_data:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user_data[0])

@app.route('/admin/users', methods=['GET'])
def get_all_users():
    records = read_csv()
    return jsonify({'status': 'success', 'data': records})

@app.route('/admin/user/<phone_number>', methods=['GET', 'DELETE'])
def get_user(phone_number):
    if request.method == 'GET':
        user_data = get_user_data(phone_number)
        if not user_data:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404
        return jsonify({'status': 'success', 'data': user_data[0]})
    
    elif request.method == 'DELETE':
        try:
            records = read_csv()
            updated_records = [r for r in records if r['phone_number'] != phone_number]
            write_csv(updated_records)
            return jsonify({'status': 'success', 'message': 'User deleted'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/status/<phone_number>/<int:year>', methods=['GET'])
def get_yearly_return(phone_number, year):
    try:
        return_data = tax_app.check_tax_return(phone_number, str(year))
        return jsonify({
            'year': year,
            'data': return_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/user/<phone_number>/year/<int:year>', methods=['GET', 'PUT'])
def handle_user_year_data(phone_number, year):
    if request.method == 'GET':
        records = get_user_data(phone_number)
        year_data = next((record for record in records if int(record['tax_year']) == year), None)
        
        if not year_data:
            return jsonify({'error': 'No data found for specified year'}), 404
            
        return jsonify({
            'status': 'success',
            'data': year_data
        })
    
    elif request.method == 'PUT':
        data = request.json
        updates = {}
        
        # Validate and process updates
        if 'income' in data:
            updates['income'] = str(float(data['income']))
        if 'expenditure' in data:
            updates['expenditure'] = str(float(data['expenditure']))
        if 'status' in data:
            updates['status'] = data['status']
        if 'tax_paid' in data:
            updates['tax_paid'] = str(float(data['tax_paid']))
            
        success = update_user_record(phone_number, year, updates)
        
        if success:
            return jsonify({'status': 'success', 'message': 'Record updated'})
        return jsonify({'error': 'Failed to update record'}), 500

@app.route('/calculate-tax/<phone_number>/<int:year>', methods=['GET'])
def calculate_tax(phone_number, year):
    try:
        records = get_user_data(phone_number)
        year_data = next((record for record in records if int(record['tax_year']) == year), None)
        
        if not year_data:
            return jsonify({'error': 'No data found for specified year'}), 404
            
        income = float(year_data['income'])
        expenses = float(year_data['expenditure'])
        taxable_income = max(0, income - expenses)
        tax_owed = calculate_nigeria_tax(taxable_income)
        
        return jsonify({
            'status': 'success',
            'data': {
                'phone_number': phone_number,
                'year': year,
                'income': income,
                'expenses': expenses,
                'taxable_income': taxable_income,
                'tax_owed': tax_owed,
                'tax_paid': float(year_data.get('tax_paid', 0))
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/check-return/<phone_number>/<int:year>', methods=['GET'])
def check_return(phone_number, year):
    try:
        user_data = get_user_data(phone_number)
        if not user_data:
            return jsonify({'error': 'User not found'}), 404
            
        year_data = next((record for record in user_data if int(record['tax_year']) == year), None)
        if not year_data:
            return jsonify({'error': 'No return filed for specified year'}), 404
            
        return jsonify({
            'status': 'success',
            'data': {
                'phone_number': phone_number,
                'year': year,
                'income': float(year_data['income']),
                'expenses': float(year_data['expenditure']),
                'tax_paid': float(year_data.get('tax_paid', 0)),
                'status': year_data['status']
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tax/<phone_number>', methods=['POST'])
def handle_tax_command(phone_number):
    try:
        data = request.json
        year = data.get('year', datetime.now().year)
        
        user_data = get_user_data(phone_number)
        if not user_data:
            return jsonify({'error': 'User not found'}), 404
            
        year_data = next((record for record in user_data if int(record['tax_year']) == year), None)
        if not year_data:
            return jsonify({'error': 'No data for specified year'}), 404
            
        income = float(year_data['income'])
        expenses = float(year_data['expenditure'])
        taxable_income = max(0, income - expenses)
        tax_owed = calculate_nigeria_tax(taxable_income)
        tax_paid = float(year_data.get('tax_paid', 0))
        
        return jsonify({
            'status': 'success',
            'data': {
                'phone_number': phone_number,
                'year': year,
                'income': income,
                'expenses': expenses,
                'taxable_income': taxable_income,
                'tax_owed': tax_owed,
                'tax_paid': tax_paid
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/return/<phone_number>', methods=['POST'])
def handle_return_command(phone_number):
    try:
        data = request.json
        year = data.get('year', datetime.now().year)
        
        user_data = get_user_data(phone_number)
        if not user_data:
            return jsonify({'error': 'User not found'}), 404
            
        year_data = next((record for record in user_data if int(record['tax_year']) == year), None)
        if not year_data:
            return jsonify({'error': 'No return filed for specified year'}), 404
            
        return jsonify({
            'status': 'success',
            'data': {
                'phone_number': phone_number,
                'year': year,
                'income': float(year_data['income']),
                'expenses': float(year_data['expenditure']),
                'tax_paid': float(year_data.get('tax_paid', 0)),
                'status': year_data['status']
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/pay-tax/<phone_number>', methods=['POST'])
def handle_tax_payment(phone_number):
    try:
        data = request.json
        year = data.get('year', datetime.now().year)
        amount = float(data.get('amount', 0))
        
        if amount <= 0:
            return jsonify({'error': 'Payment amount must be greater than 0'}), 400
            
        records = read_csv()
        year_data = next((record for record in records 
                         if record['phone_number'] == phone_number 
                         and record['tax_year'] == str(year)), None)
        
        if not year_data:
            return jsonify({'error': 'No tax record found for specified year'}), 404
            
        # Update the tax_paid amount
        current_paid = float(year_data.get('tax_paid', 0))
        year_data['tax_paid'] = str(current_paid + amount)
        
        # Calculate remaining tax
        income = float(year_data['income'])
        expenses = float(year_data['expenditure'])
        taxable_income = max(0, income - expenses)
        total_tax = calculate_nigeria_tax(taxable_income)
        remaining_tax = max(0, total_tax - (current_paid + amount))
        
        # Update status if tax is fully paid
        if remaining_tax <= 0:
            year_data['status'] = 'paid'
        
        write_csv(records)
        
        return jsonify({
            'status': 'success',
            'data': {
                'year': year,
                'amount_paid': amount,
                'total_paid': current_paid + amount,
                'total_tax': total_tax,
                'remaining_tax': remaining_tax,
                'status': year_data['status']
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/update-user', methods=['POST'])
def update_user_data():
    try:
        data = request.json
        if not data:
            return jsonify({'status': 'error', 'message': 'No data provided'}), 400

        # Validate required fields
        required_fields = ['phone_number', 'tax_year', 'income', 'tax_paid']
        for field in required_fields:
            if field not in data:
                return jsonify({'status': 'error', 'message': f'Missing required field: {field}'}), 400

        # Read current data
        records = read_csv()
        
        # Calculate tax owed based on income and expenditure
        income = float(data['income'])
        expenditure = float(data.get('expenditure', 0))
        taxable_income = max(0, income - expenditure)
        tax_owed = calculate_nigeria_tax(taxable_income)
        
        # Find the record to update
        record_found = False
        for record in records:
            if (record['phone_number'] == data['phone_number'] and 
                record['tax_year'] == str(data['tax_year'])):
                
                # Update the record
                record.update({
                    'income': str(income),
                    'expenditure': str(expenditure),
                    'tax_paid': str(data['tax_paid']),
                    'tin': data.get('tin', record.get('tin', '')),
                    'tax_code': data.get('tax_code', record.get('tax_code', f"TAX-{data['phone_number'][-6:]}")),
                    'tax_owed': str(tax_owed)
                })
                
                # Update status based on tax paid vs tax owed
                tax_paid = float(data['tax_paid'])
                
                if tax_paid >= tax_owed:
                    record['status'] = 'paid'
                elif tax_paid > 0:
                    record['status'] = 'active'
                else:
                    record['status'] = 'pending'
                
                record_found = True
                break

        # If record not found, create new one
        if not record_found:
            new_record = {
                'phone_number': data['phone_number'],
                'tax_year': str(data['tax_year']),
                'income': str(income),
                'expenditure': str(expenditure),
                'tax_paid': str(data['tax_paid']),
                'tin': data.get('tin', ''),
                'tax_code': data.get('tax_code', f"TAX-{data['phone_number'][-6:]}"),
                'tax_owed': str(tax_owed),
                'status': 'pending'
            }
            
            # Set status based on tax paid vs tax owed
            tax_paid = float(data['tax_paid'])
            
            if tax_paid >= tax_owed:
                new_record['status'] = 'paid'
            elif tax_paid > 0:
                new_record['status'] = 'active'
            
            records.append(new_record)

        # Write updated data back to CSV
        write_csv(records)
        
        return jsonify({
            'status': 'success',
            'message': 'User data updated successfully',
            'data': {
                **data,
                'tax_owed': tax_owed,
                'status': 'paid' if float(data['tax_paid']) >= tax_owed else 
                         'active' if float(data['tax_paid']) > 0 else 'pending'
            }
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to update user data: {str(e)}'
        }), 500

@app.route('/')
def index():
    return jsonify({
        'status': 'success',
        'message': 'Mock server is running'
    })

# Add a function to ensure CSV file exists with correct headers
def ensure_csv_exists():
    if not os.path.exists('data'):
        os.makedirs('data')
    
    if not os.path.exists(CSV_FILE):
        fieldnames = ['phone_number', 'tin', 'tax_year', 'income', 'expenditure', 
                     'status', 'tax_code', 'tax_paid']
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

# Call ensure_csv_exists when the server starts
if __name__ == '__main__':
    ensure_csv_exists()
    print("Starting mock server on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000) 