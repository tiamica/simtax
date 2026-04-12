FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

# Create non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create a combined launcher script
RUN cat > /app/launcher.py <<'EOF'
#!/usr/bin/env python3
import subprocess
import sys
import os

# Get port from environment (Cloud Run sets this)
port = os.environ.get('PORT', '8080')

# Start both Flask apps
processes = [
    subprocess.Popen([sys.executable, 'mockserver.py'], 
                     env={**os.environ, 'PORT': '5000'}),
    subprocess.Popen([sys.executable, 'web_interface.py'],
                     env={**os.environ, 'PORT': '5001'})
]

# Wait for both processes
for p in processes:
    p.wait()
EOF

RUN chmod +x /app/launcher.py

# Create simple nginx config (install nginx)
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/* && \
    cat > /etc/nginx/sites-available/default <<'NGINX'
server {
    listen 8080;
    
    location ~ ^/(send|status|calculate-tax) {
        proxy_pass http://127.0.0.1:5000;
    }
    
    location / {
        proxy_pass http://127.0.0.1:5001;
    }
}
NGINX

# Fix permissions
RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8080

# Start nginx and the Python apps
CMD nginx -g "daemon off;" & python /app/launcher.py
