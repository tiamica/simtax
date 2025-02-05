from flask import Flask, request, jsonify
from tax_app import TaxApp
import threading
import time

app = Flask(__name__)
tax_app = TaxApp()

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
    response = tax_app.check_status(phone_number)
    return jsonify({'status': response})

# Start the server
if __name__ == '__main__':
    shortcode_provider = MockShortcodeProvider()
    shortcode_provider.start()
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        shortcode_provider.stop() 