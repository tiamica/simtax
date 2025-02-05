from tax_app import TaxApp
import time

class ShortcodeHandler:
    def __init__(self):
        self.tax_app = TaxApp()
        
    def handle_message(self, phone_number, message):
        response = self.tax_app.process_message(phone_number, message)
        # Here you would integrate with your shortcode provider's API
        # to send the response back to the user
        self.send_sms(phone_number, response)
        
    def send_sms(self, phone_number, message):
        # This would be replaced with actual SMS sending code
        print(f"Sending to {phone_number}: {message}")

# Example usage
handler = ShortcodeHandler()
handler.handle_message("+2348123456789", "REG 123456789")
handler.handle_message("+2348123456789", "INC 500000")
handler.handle_message("+2348123456789", "EXP 200000")
handler.handle_message("+2348123456789", "TAX")
handler.handle_message("+2348123456789", "PAY 45000")
handler.handle_message("+2348123456789", "STATUS") 