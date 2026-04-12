# Use Python slim image as base
FROM python:3.11-slim

# Install nginx and supervisor
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    supervisor \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # External port (Cloud Run injects $PORT, fallback to 8080)
    PORT=8080

# Create a non‑root user for security
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Set work directory
WORKDIR /app

# Copy Python dependencies first (for better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code
COPY . .

# Fix ownership for the non‑root user
RUN chown -R appuser:appgroup /app

# --- Configure nginx ---
# Remove default nginx site
RUN rm /etc/nginx/sites-enabled/default

# Write custom nginx config that uses $PORT and proxies to the two backends
RUN cat > /etc/nginx/sites-available/simtax <<'EOF'
server {
    listen ${PORT} default_server;
    server_name _;

    # Increase max body size for file uploads (if needed)
    client_max_body_size 10M;

    # Proxy API endpoints to mockserver (port 5000)
    location ~ ^/(send|status|calculate-tax) {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # Proxy everything else to web_interface (port 5001)
    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
EOF

# Enable the site and substitute the PORT variable at runtime
RUN ln -s /etc/nginx/sites-available/simtax /etc/nginx/sites-enabled/

# Replace the $PORT placeholder in nginx config with the environment variable
# (We'll do this at runtime using envsubst, but we can also create a wrapper script)
COPY <<'SCRIPT' /docker-entrypoint.sh
#!/bin/bash
set -e

# Substitute $PORT in the nginx config with the actual environment variable
envsubst '${PORT}' < /etc/nginx/sites-available/simtax > /etc/nginx/sites-available/simtax.tmp
mv /etc/nginx/sites-available/simtax.tmp /etc/nginx/sites-available/simtax

# Start supervisord (manages nginx and the two Python apps)
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
SCRIPT

RUN chmod +x /docker-entrypoint.sh

# --- Configure supervisor ---
RUN cat > /etc/supervisor/conf.d/supervisord.conf <<'EOF'
[supervisord]
nodaemon=true
user=root
logfile=/dev/stdout
logfile_maxbytes=0

[program:nginx]
command=/usr/sbin/nginx -g "daemon off;"
autostart=true
autorestart=true
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0

[program:mockserver]
command=python /app/mockserver.py
user=appuser
autostart=true
autorestart=true
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0
environment=PORT="5000"

[program:webinterface]
command=python /app/web_interface.py
user=appuser
autostart=true
autorestart=true
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0
environment=PORT="5001"
EOF

# Ensure the non‑root user has write access to nginx logs (if needed)
RUN touch /var/log/nginx/access.log /var/log/nginx/error.log && \
    chown -R appuser:appgroup /var/log/nginx /var/lib/nginx /run/nginx.pid

# Expose the external port (Cloud Run will use $PORT)
EXPOSE ${PORT}

# Use the custom entrypoint
ENTRYPOINT ["/docker-entrypoint.sh"]
