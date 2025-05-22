class TaxApp:
    def __init__(self):
        self.users = {}
        self.tax_rate = 0.15  # 15% tax rate
        # Add tax code and yearly returns storage
        self.tax_codes = {}
        self.yearly_returns = {}
        self.outstanding_balances = {}  # Track outstanding tax amounts

    def generate_tax_code(self, phone_number):
        """Generate a unique tax code based on phone number"""
        import hashlib
        # Create a hash of the phone number and take first 8 characters
        return "TAX-" + hashlib.sha256(phone_number.encode()).hexdigest()[:8].upper()

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
        
        # Generate and store unique tax code
        tax_code = self.generate_tax_code(phone_number)
        self.tax_codes[phone_number] = tax_code
        
        self.users[phone_number] = {
            'tin': tin,
            'income': 0,
            'expenses': 0,
            'payments': 0,
            'status': 'registered',
            'tax_code': tax_code
        }
        return f"Registration successful! Your tax code is {tax_code}"

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
        if taxable_income < 0:
            return "No tax liability (negative taxable income)"
        
        # Calculate tax using Nigerian rates
        tax = self.calculate_nigeria_tax(taxable_income)
        
        # Add any outstanding balance
        outstanding = self.outstanding_balances.get(phone_number, 0)
        total_tax = tax + outstanding
        
        return f"Your tax liability is ₦{total_tax:,.2f} (including ₦{outstanding:,.2f} outstanding). Send PAY <amount> to make payment."

    def calculate_nigeria_tax(self, taxable_income):
        tax = 0
        remaining_income = taxable_income
        
        for threshold, rate in [
            (300000, 0.07),    # First 300,000 at 7%
            (300000, 0.11),    # Next 300,000 at 11%
            (500000, 0.15),    # Next 500,000 at 15%
            (500000, 0.19),    # Next 500,000 at 19%
            (1600000, 0.21),   # Next 1,600,000 at 21%
            (3200000, 0.24)    # Above 3,200,000 at 24%
        ]:
            if remaining_income <= 0:
                break
            amount = min(threshold, remaining_income)
            tax += amount * rate
            remaining_income -= amount
        
        # Apply 24% for any amount above the last threshold
        if remaining_income > 0:
            tax += remaining_income * 0.24
        
        return tax

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
        return f"Your tax code is: {user['tax_code']}"

    def check_tax_return(self, phone_number, year):
        user = self.users.get(phone_number)
        if not user:
            return "Please register first using REG <TIN>"
        
        # Validate year
        current_year = datetime.datetime.now().year
        if not (2019 <= int(year) <= current_year + 1):  # Allow one year in future
            return "Invalid year. Please enter a year between 2019 and " + str(current_year + 1)
        
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