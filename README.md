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
- `INC <amount>`: Report income
- `EXP <amount>`: Report expense
- `TAX`: Calculate tax
- `PAY <amount>`: Make payment
- `STATUS`: Check status
- `CODE`: Check tax code
- `RETURN <year>`: Check tax return
- `PAYRETURN <year> <amount>`: Pay tax return

### Web Interface
Access at `http://localhost:5001`
- View tax accounts
- Check status and returns

### Mobile Simulator
Open `mobile-simulator.html` in your browser
- Simulate shortcode interactions
- View responses in chat format

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

2. Calculate Tax:
   ```bash
   curl -X POST http://localhost:5000/calculate-tax \
       -d '{"taxable_income": 1000000}'
   ```

3. View Account:
   Open `http://localhost:5001` in browser 