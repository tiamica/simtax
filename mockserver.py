from flask import Flask, request, jsonify
from tax_app import TaxApp
import threading
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
tax_app = TaxApp()

# Nigerian Personal Income Tax Rates (2023)
TAX_RATES = [
    (300000, 0.07),    # First 300,000 at 7%
    (300000, 0.11),    # Next 300,000 at 11%
    (500000, 0.15),    # Next 500,000 at 15%
    (500000, 0.19),    # Next 500,000 at 19%
    (1600000, 0.21),   # Next 1,600,000 at 21%
    (3200000, 0.24)    # Above 3,200,000 at 24%
]

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
def send_message():
    data = request.json
    phone_number = data.get('phone_number')
    message = data.get('message')
    
    if not phone_number or not message:
        return jsonify({'error': 'phone_number and message are required'}), 400
    
    shortcode_provider.receive_message(phone_number, message)
    return jsonify({'status': 'message received'})

@app.route('/status/<phone_number>', methods=['GET'])
def get_status(phone_number):
    try:
        status = tax_app.check_status(phone_number)
        tax_code = tax_app.check_tax_code(phone_number)
        return jsonify({
            'phone_number': phone_number,
            'status': status,
            'tax_code': tax_code
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

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

@app.route('/calculate-tax', methods=['POST'])
def calculate_tax():
    data = request.json
    taxable_income = float(data.get('taxable_income', 0))
    
    if taxable_income < 0:
        return jsonify({'error': 'Taxable income cannot be negative'}), 400
    
    tax = calculate_nigeria_tax(taxable_income)
    return jsonify({
        'taxable_income': taxable_income,
        'tax': tax
    })

# Start the server
if __name__ == '__main__':
    shortcode_provider = MockShortcodeProvider()
    shortcode_provider.start()
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        shortcode_provider.stop() 