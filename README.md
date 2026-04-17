# SimTax — Nigerian Tax Collection Simulator

A simulation of a shortcode-based tax collection system using Nigerian Personal Income Tax rates.

## Architecture

| Component | Description |
|---|---|
| `mockserver.py` | Flask REST API (port 5000) — handles shortcode commands and tax data |
| `web_interface.py` | Flask web app (port 5001) — account viewer |
| `tax-web-ui/` | Static HTML — mobile simulator and admin dashboard |
| `tax_app.py` | Core tax logic (registration, calculation, payments) |
| `data/tax_data.csv` | Persistent data store |

nginx (port 8080) sits in front of all three, routing API calls to the mock server, web requests to the web interface, and serving the static UI files under `/ui/`.

## Running with Docker (recommended)

```bash
docker build -t simtax:latest .
docker run -d --name simtax --network host simtax:latest
```

> `--network host` is required so the Gitpod/cloud proxy can reach the container on port 8080.

## Running locally (without Docker)

```bash
pip install -r requirements.txt
python mockserver.py     # terminal 1 — API on port 5000
python web_interface.py  # terminal 2 — web interface on port 5001
```

Open `tax-web-ui/mobile-simulator.html` and `tax-web-ui/admin.html` directly in your browser.

## Accessing the application

Once running, all interfaces are available on port 8080:

| Interface | Path |
|---|---|
| Web Interface | `/` |
| Mobile Simulator | `/ui/mobile-simulator.html` |
| Admin Dashboard | `/ui/admin.html` |

Admin login: username `admin`, password `admin`.

## Shortcode commands

Commands are sent via the mobile simulator or the `/send` API endpoint.

| Command | Description |
|---|---|
| `REG <TIN>` | Register with Tax Identification Number |
| `INC <amount> [year]` | Report income |
| `EXP <amount> [year]` | Report expense |
| `YEAR [year]` | Set or view the current tax year |
| `TAX [year]` | Calculate tax liability |
| `PAY <amount> [year]` | Make a tax payment |
| `RETURN [year]` | View tax return |
| `STATUS` | Check account status |
| `CODE` | View your tax code |
| `PAYRETURN <year> <amount>` | Pay tax return for a specific year |

Commands that accept a `year` parameter use the year set by `YEAR` if not explicitly provided. The default is the current calendar year.

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/send` | Send a shortcode command (`REG`, `INC`, `EXP`, `PAY`) |
| GET | `/status/<phone>` | Get account status |
| GET | `/status/<phone>/<year>` | Get yearly return data |
| POST | `/tax/<phone>` | Calculate tax for a year |
| POST | `/return/<phone>` | Get tax return for a year |
| POST | `/pay-tax/<phone>` | Record a tax payment |
| GET | `/admin/users` | List all users |
| GET/DELETE | `/admin/user/<phone>` | Get or delete a user |
| POST | `/admin/update-user` | Update user data |
| GET | `/calculate-tax/<phone>/<year>` | Calculate tax (alternative endpoint) |

### Example API usage

```bash
# Register
curl -X POST http://localhost:8080/send \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+2348123456789", "message": "REG 123456789"}'

# Report income
curl -X POST http://localhost:8080/send \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+2348123456789", "message": "INC 5000000 2026"}'

# Calculate tax
curl -X POST http://localhost:8080/tax/%2B2348123456789 \
  -H "Content-Type: application/json" \
  -d '{"year": 2026}'

# Make payment
curl -X POST http://localhost:8080/pay-tax/%2B2348123456789 \
  -H "Content-Type: application/json" \
  -d '{"amount": 500000, "year": 2026}'

# Check status
curl http://localhost:8080/status/%2B2348123456789
```

## Tax rates

Nigerian Personal Income Tax rates (2023):

| Band | Rate |
|---|---|
| First ₦300,000 | 7% |
| Next ₦300,000 | 11% |
| Next ₦500,000 | 15% |
| Next ₦500,000 | 19% |
| Next ₦1,600,000 | 21% |
| Above ₦3,200,000 | 24% |

## Test accounts

Five pre-seeded accounts are available for testing:

| Phone | TIN | Tax Code |
|---|---|---|
| +2348123456789 | 123456789 | TAX-ABC123 |
| +2348123456790 | 123456790 | TAX-DEF456 |
| +2348123456791 | 123456791 | TAX-GHI789 |
| +2348123456792 | 123456792 | TAX-JKL012 |
| +2348123456793 | 123456793 | TAX-MNO345 |

## Dependencies

| Package | Version | Notes |
|---|---|---|
| Flask | 2.3.2 | |
| Flask-Bootstrap | 3.3.7.1 | |
| Flask-WTF | 1.2.1 | Upgraded from 1.1.1 — incompatible with Werkzeug 3.x |
| WTForms | 3.0.1 | |
| Werkzeug | 2.3.7 | Downgraded from 3.0.1 — `url_encode` removed in 3.x |
| Flask-CORS | 4.0.0 | |
| requests | 2.31.0 | |
