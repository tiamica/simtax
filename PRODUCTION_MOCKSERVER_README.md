# Production Mock Server Setup Guide

This guide provides instructions for setting up the Tax App Mock Server in production mode with HTTPS on a Google Cloud Platform (GCP) VM.

## Overview

The production version of the mockserver runs with the following features:
- HTTPS for secure communication
- Proper logging and error handling
- Data persistence across server restarts
- Runs as a system service that automatically starts on boot
- Health check endpoint for monitoring

## Prerequisites

- A GCP VM instance running Ubuntu (recommended Ubuntu 20.04 LTS or later)
- Public IP address (34.173.20.218 is used in this example)
- Basic knowledge of Linux server administration

## Deployment Steps

### 1. Set Up the GCP VM

1. Create a GCP VM instance:
   - Machine type: e2-medium or higher
   - Boot disk: Ubuntu 20.04 LTS
   - Allow HTTPS traffic in the firewall rules

2. Connect to your VM via SSH

3. Upload the necessary files to the VM:
   ```
   scp mockserver_production.py mockserver.service setup_production_server.sh tax_app.py user@34.173.20.218:~/
   ```

4. Make the setup script executable:
   ```
   chmod +x setup_production_server.sh
   ```

5. Run the setup script:
   ```
   sudo ./setup_production_server.sh
   ```

### 2. Verify the Installation

1. Check if the service is running:
   ```
   sudo systemctl status mockserver.service
   ```

2. Test the HTTPS endpoint:
   ```
   curl -k https://34.173.20.218:5000/health
   ```

3. Check the logs:
   ```
   sudo journalctl -u mockserver.service
   ```

### 3. Security Considerations

- The default setup uses a self-signed certificate, which is sufficient for testing but may cause browser warnings
- For a production environment with a domain name, uncomment the certbot line in the setup script to obtain a Let's Encrypt certificate
- Keep your server updated regularly with security patches
- Consider adding authentication for the admin endpoints

## Configuration Files

### mockserver_production.py
The main server implementation file with HTTPS support and production-grade features.

### mockserver.service
The systemd service definition that ensures the server runs automatically.

### setup_production_server.sh
A setup script that configures the VM with all required dependencies and settings.

## Directory Structure

- `/opt/taxapp/` - Application files
- `/var/data/taxapp/` - Data files (CSV database)
- `/var/log/taxapp/` - Log files
- `/etc/ssl/certs/mockserver.crt` - SSL certificate
- `/etc/ssl/private/mockserver.key` - SSL private key

## Maintenance

### Restarting the Server
```
sudo systemctl restart mockserver.service
```

### Viewing Logs
```
sudo journalctl -u mockserver.service
```

### Updating the Application
1. Upload the new version to the VM
2. Copy it to the application directory:
   ```
   sudo cp mockserver_production.py /opt/taxapp/
   ```
3. Restart the service:
   ```
   sudo systemctl restart mockserver.service
   ```

## Troubleshooting

1. **Server won't start:**
   - Check logs: `sudo journalctl -u mockserver.service -n 50`
   - Verify permissions: `sudo ls -la /opt/taxapp/`
   - Ensure Python dependencies are installed: `pip3 list`

2. **HTTPS not working:**
   - Verify certificate exists: `sudo ls -la /etc/ssl/certs/mockserver.crt`
   - Check firewall rules: `sudo ufw status`
   - Ensure the service is binding to the correct address: `sudo netstat -tulpn | grep 5000`

3. **Cannot write to data file:**
   - Check permissions: `sudo ls -la /var/data/taxapp/`
   - Verify the taxapp user exists: `getent passwd taxapp`

## API Endpoints

All endpoints are the same as the development version but now run securely over HTTPS:

- `https://34.173.20.218:5000/health` - Health check endpoint
- `https://34.173.20.218:5000/send` - Send messages to the mock server
- `https://34.173.20.218:5000/admin/users` - Get all users
- `https://34.173.20.218:5000/admin/user/<phone_number>` - Get/delete specific user
- `https://34.173.20.218:5000/tax/<phone_number>` - Tax calculation
- `https://34.173.20.218:5000/return/<phone_number>` - Tax return status
- `https://34.173.20.218:5000/pay-tax/<phone_number>` - Process tax payment 