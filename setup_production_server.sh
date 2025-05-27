#!/bin/bash
# Setup script for Tax App Mock Server on GCP VM
# Run as root or with sudo

set -e  # Exit on any error

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root or with sudo"
  exit 1
fi

echo "Setting up Tax App Mock Server in production mode..."

# Update and install dependencies
echo "Updating system and installing dependencies..."
apt-get update
apt-get upgrade -y
apt-get install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx

# Create application user
echo "Creating application user..."
useradd -m -s /bin/bash taxapp || echo "User taxapp already exists"

# Create application directory structure
echo "Creating directory structure..."
mkdir -p /opt/taxapp
mkdir -p /var/data/taxapp
mkdir -p /var/log/taxapp

# Set permissions
echo "Setting permissions..."
chown -R taxapp:taxapp /opt/taxapp
chown -R taxapp:taxapp /var/data/taxapp
chown -R taxapp:taxapp /var/log/taxapp

# Copy application files
echo "Copying application files..."
cp mockserver_production.py /opt/taxapp/
cp tax_app.py /opt/taxapp/  # Make sure this file exists
cp -r templates /opt/taxapp/ || echo "No templates directory found"
cp -r static /opt/taxapp/ || echo "No static directory found"

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install flask flask-cors gunicorn

# Setup systemd service
echo "Setting up systemd service..."
cp mockserver.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable mockserver.service

# Generate SSL certificate with certbot
echo "Setting up SSL certificate..."
# Uncomment the following line and replace with your domain if you have one
# certbot --nginx -d yourdomain.com -d www.yourdomain.com

# If using self-signed certificate for testing
echo "Generating self-signed SSL certificate..."
mkdir -p /etc/ssl/certs
mkdir -p /etc/ssl/private
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/mockserver.key \
  -out /etc/ssl/certs/mockserver.crt \
  -subj "/C=NG/ST=Lagos/L=Lagos/O=Fourier Analytics/OU=IT/CN=34.173.20.218"

# Configure firewall to allow HTTPS traffic
echo "Configuring firewall..."
ufw allow 22/tcp  # SSH
ufw allow 443/tcp  # HTTPS
ufw allow 5000/tcp  # Mock server port
ufw --force enable

# Start the service
echo "Starting the mock server service..."
systemctl start mockserver.service

# Display status
echo "Service status:"
systemctl status mockserver.service

echo "Setup complete!"
echo "Mock server should be running on https://34.173.20.218:5000"
echo "Check /var/log/syslog or journalctl -u mockserver.service for logs" 