class TaxApp:
    def __init__(self):
        self.users = {}
        self.tax_rate = 0.15  # 15% tax rate
        # Add tax code and yearly returns storage
        self.tax_codes = {}
        self.yearly_returns = {}

    def process_message(self, phone_number, message):
        try:
            parts = message.strip().split()
            command = parts[0].upper()
            
            if command == "REG":
                return self.register_user(phone_number, parts[1])
            elif command == "INC":
                return self.record_income(phone_number, float(parts[1]))
            elif command == "EXP":
                return self.record_expense(phone_number, float(parts[1]))
            elif command == "TAX":
                return self.calculate_tax(phone_number)
            elif command == "PAY":
                return self.make_payment(phone_number, float(parts[1]))
            elif command == "STATUS":
                return self.check_status(phone_number)
            elif command == "CODE":
                return self.check_tax_code(phone_number)
            elif command == "RETURN":
                return self.check_tax_return(phone_number, parts[1])
            elif command == "PAYRETURN":
                return self.pay_tax_return(phone_number, parts[1], float(parts[2]))
            else:
                return "Invalid command. Please try again."
        except Exception as e:
            return f"Error: {str(e)}"

    def register_user(self, phone_number, tin):
        if phone_number in self.users:
            return "You are already registered."
        self.users[phone_number] = {
            'tin': tin,
            'income': 0,
            'expenses': 0,
            'payments': 0,
            'status': 'registered'
        }
        return "Registration successful! Welcome to TaxApp."

    def record_income(self, phone_number, amount):
        user = self.users.get(phone_number)
        if not user:
            return "Please register first using REG <TIN>"
        user['income'] += amount
        return f"Income of ₦{amount:,.2f} recorded."

    def record_expense(self, phone_number, amount):
        user = self.users.get(phone_number)
        if not user:
            return "Please register first using REG <TIN>"
        user['expenses'] += amount
        return f"Expense of ₦{amount:,.2f} recorded."

    def calculate_tax(self, phone_number):
        user = self.users.get(phone_number)
        if not user:
            return "Please register first using REG <TIN>"
        taxable_income = user['income'] - user['expenses']
        tax = max(0, taxable_income * self.tax_rate)
        return f"Your tax liability is ₦{tax:,.2f}. Send PAY <amount> to make payment."

    def make_payment(self, phone_number, amount):
        user = self.users.get(phone_number)
        if not user:
            return "Please register first using REG <TIN>"
        user['payments'] += amount
        user['status'] = 'paid'
        return f"Payment of ₦{amount:,.2f} successful. Your tax return is complete."

    def check_status(self, phone_number):
        user = self.users.get(phone_number)
        if not user:
            return "Please register first using REG <TIN>"
        return f"Status: {user['status']}. Income: ₦{user['income']:,.2f}, Expenses: ₦{user['expenses']:,.2f}, Payments: ₦{user['payments']:,.2f}"

    def check_tax_code(self, phone_number):
        user = self.users.get(phone_number)
        if not user:
            return "Please register first using REG <TIN>"
        tax_code = self.tax_codes.get(phone_number, "TAX-CODE-12345")
        return f"Your tax code is: {tax_code}"

    def check_tax_return(self, phone_number, year):
        user = self.users.get(phone_number)
        if not user:
            return "Please register first using REG <TIN>"
        
        return_data = self.yearly_returns.get((phone_number, year), {
            'income': 0,
            'expenses': 0,
            'tax_paid': 0,
            'status': 'No return filed'
        })
        
        return (f"Tax return for {year}:\n"
                f"Income: ₦{return_data['income']:,.2f}\n"
                f"Expenses: ₦{return_data['expenses']:,.2f}\n"
                f"Tax Paid: ₦{return_data['tax_paid']:,.2f}\n"
                f"Status: {return_data['status']}")

    def pay_tax_return(self, phone_number, year, amount):
        user = self.users.get(phone_number)
        if not user:
            return "Please register first using REG <TIN>"
        
        key = (phone_number, year)
        if key not in self.yearly_returns:
            self.yearly_returns[key] = {
                'income': user['income'],
                'expenses': user['expenses'],
                'tax_paid': 0,
                'status': 'Pending'
            }
        
        self.yearly_returns[key]['tax_paid'] += amount
        self.yearly_returns[key]['status'] = 'Paid'
        return f"Payment of ₦{amount:,.2f} for {year} tax return successful." 