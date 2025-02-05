# Tax Collection App - Shortcode System

This project provides a mock tax collection system that can be accessed via shortcodes. It includes a mock server that simulates the tax system and handles shortcode interactions.

## Features

1. **Shortcode Commands:**
   - `REG <TIN>`: Register with Tax Identification Number
   - `INC <amount>`: Report income
   - `EXP <amount>`: Report expense
   - `TAX`: Calculate and return tax amount
   - `PAY <amount>`: Make payment
   - `STATUS`: Check tax return status
   - `CODE`: Check tax code
   - `RETURN <year>`: Check tax return for a specific year
   - `PAYRETURN <year> <amount>`: Pay tax return for a specific year

2. **Mock Server:**
   - Simulates a shortcode provider
   - Provides API endpoints for testing
   - Processes messages in real-time

## Setup

1. Create a Python virtual environment (Python 3.8+ recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the mock server:
   ```bash
   python mockserver.py
   ```

4. The server will be available at `http://localhost:5000`

## API Endpoints

- **POST /send**
  Send a shortcode message
  ```json
  {
      "phone_number": "+2348123456789",
      "message": "REG 123456789"
  }
  ```

- **GET /status/<phone_number>**
  Get current tax status for a user

## Example Usage

1. Register:
   ```bash
   curl -X POST http://localhost:5000/send \
       -H "Content-Type: application/json" \
       -d '{"phone_number": "+2348123456789", "message": "REG 123456789"}'
   ```

2. Report income:
   ```bash
   curl -X POST http://localhost:5000/send \
       -H "Content-Type: application/json" \
       -d '{"phone_number": "+2348123456789", "message": "INC 500000"}'
   ```

3. Check tax code:
   ```bash
   curl -X POST http://localhost:5000/send \
       -H "Content-Type: application/json" \
       -d '{"phone_number": "+2348123456789", "message": "CODE"}'
   ```

4. Check tax return for 2023:
   ```bash
   curl -X POST http://localhost:5000/send \
       -H "Content-Type: application/json" \
       -d '{"phone_number": "+2348123456789", "message": "RETURN 2023"}'
   ```

5. Pay tax return for 2023:
   ```bash
   curl -X POST http://localhost:5000/send \
       -H "Content-Type: application/json" \
       -d '{"phone_number": "+2348123456789", "message": "PAYRETURN 2023 45000"}'
   ```

## Implementation Details

The system consists of:
- `tax_app.py`: Core tax application logic
- `mockserver.py`: Mock server implementation
- `shortcode_integration.py`: Shortcode handler

## Testing

You can test the system using curl commands or Postman. The mock server will print all responses to the console.

## Future Enhancements

1. Add database persistence
2. Implement actual SMS integration
3. Add authentication and security
4. Implement more sophisticated tax calculation rules
5. Add error handling and validation 