# Tax Collection App

## Features

1. **Shortcode System**
2. **Web Interface**
3. **Mobile Simulator**
4. **Admin Dashboard**

## Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Mock Server:**
   ```bash
   python mockserver.py
   ```

3. **Start the Web Interface:**
   ```bash
   python web_interface.py
   ```

## Usage

### Shortcode Commands
Access via mobile simulator or API:
- `REG <TIN>`: Register with Tax Identification Number
- `INC <amount> [year]`: Report income (optionally specify the tax year)
- `EXP <amount> [year]`: Report expense (optionally specify the tax year)
- `YEAR <year>`: Set the current tax year for all operations (or view current year if no parameter)
- `TAX [year]`: Calculate tax liability (optionally for a specific year)
- `PAY <amount> [year]`: Make tax payment (optionally for a specific year)
- `STATUS`: Check account status
- `CODE`: Check your tax code
- `RETURN [year]`: Check tax return (defaults to current year if not specified)
- `PAYRETURN <year> <amount>`: Pay tax return for a specific year

All commands that accept a year parameter will use the year set by the `YEAR` command if not explicitly provided. The default tax year is set to the current calendar year.

### Web Interface
Access at `http://localhost:5001`
- View tax accounts
- Check status and returns

### Mobile Simulator
Open `tax-web-ui/mobile-simulator.html` in your browser
- Simulate shortcode interactions
- View responses in chat format
- Set and change tax year for all operations
- Enter commands and see immediate responses
- Press Enter to quickly send commands

### User Experience Features
- **Keyboard Shortcuts**:
  - Press Enter to submit commands in the mobile simulator
  - Press Enter to login with your phone number
- **Tax Year Management**:
  - Current tax year is displayed when you log in
  - Tax year is remembered for all operations until changed
  - Tax year resets to current calendar year on logout
- **Response Formatting**:
  - Tax calculation responses include the tax year
  - Income and expense entries show which tax year they apply to
  - Payment status is correctly calculated based on tax owed vs. tax paid

### Admin Dashboard
Open `admin.html` in your browser
- Login with username: `admin`, password: `admin`
- View and manage all user accounts
- Update user information
- Delete accounts
- Access detailed tax information for each user
- Manage tax rates and configurations

To access the admin tool:
1. Open the `tax-web-ui` folder
2. Double-click `admin.html` to open in your browser
3. Login with username: `admin` and password: `admin`
4. Use the dashboard to manage user accounts and tax data

### Test Accounts
The system includes 5 dummy accounts for testing:

1. **+2348123456789** - TIN: 123456789 - Tax Code: TAX-ABC123
2. **+2348123456790** - TIN: 123456790 - Tax Code: TAX-DEF456
3. **+2348123456791** - TIN: 123456791 - Tax Code: TAX-GHI789
4. **+2348123456792** - TIN: 123456792 - Tax Code: TAX-JKL012
5. **+2348123456793** - TIN: 123456793 - Tax Code: TAX-MNO345

These accounts have pre-filled data for testing all features of the system.

## API Endpoints

- **POST /send** - Send shortcode message
- **GET /status/<phone_number>** - Get user status
- **POST /calculate-tax** - Calculate tax

## Example Usage

1. Register:
   ```bash
   curl -X POST http://localhost:5000/send \
       -d '{"phone_number": "+2348123456789", "message": "REG 123456789"}'
   ```

2. Set Tax Year:
   ```bash
   curl -X POST http://localhost:5000/send \
       -d '{"phone_number": "+2348123456789", "message": "YEAR 2023"}'
   ```

3. Report Income:
   ```bash
   curl -X POST http://localhost:5000/send \
       -d '{"phone_number": "+2348123456789", "message": "INC 5000000"}'
   ```

4. Report Expenses:
   ```bash
   curl -X POST http://localhost:5000/send \
       -d '{"phone_number": "+2348123456789", "message": "EXP 2000000"}'
   ```

5. Calculate Tax:
   ```bash
   curl -X POST http://localhost:5000/send \
       -d '{"phone_number": "+2348123456789", "message": "TAX"}'
   ```

6. Make Payment:
   ```bash
   curl -X POST http://localhost:5000/send \
       -d '{"phone_number": "+2348123456789", "message": "PAY 500000"}'
   ```

7. View in Web Interface:
   Open `http://localhost` in browser 