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
    PORT=8080

# Create a non-root user for security
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Set work directory
WORKDIR /app

# Copy Python dependencies first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code
COPY . .

# Fix ownership
RUN chown -R appuser:appgroup /app

# Create nginx configuration (using echo commands)
RUN echo 'server {' > /etc/nginx/sites-available/simtax && \
    echo '    listen 8080 default_server;' >> /etc/nginx/sites-available/simtax && \
    echo '    server_name _;' >> /etc/nginx/sites-available/simtax && \
    echo '    client_max_body_size 10M;' >> /etc/nginx/sites-available/simtax && \
    echo '' >> /etc/nginx/sites-available/simtax && \
    echo '    location ~ ^/(send|status|calculate-tax) {' >> /etc/nginx/sites-available/simtax && \
    echo '        proxy_pass http://127.0.0.1:5000;' >> /etc/nginx/sites-available/simtax && \
    echo '        proxy_set_header Host $host;' >> /etc/nginx/sites-available/simtax && \
    echo '        proxy_set_header X-Real-IP $remote_addr;' >> /etc/nginx/sites-available/simtax && \
    echo '        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;' >> /etc/nginx/sites-available/simtax && \
    echo '    }' >> /etc/nginx/sites-available/simtax && \
    echo '' >> /etc/nginx/sites-available/simtax && \
    echo '    location / {' >> /etc/nginx/sites-available/simtax && \
    echo '        proxy_pass http://127.0.0.1:5001;' >> /etc/nginx/sites-available/simtax && \
    echo '        proxy_set_header Host $host;' >> /etc/nginx/sites-available/simtax && \
    echo '        proxy_set_header X-Real-IP $remote_addr;' >> /etc/nginx/sites-available/simtax && \
    echo '        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;' >> /etc/nginx/sites-available/simtax && \
    echo '    }' >> /etc/nginx/sites-available/simtax && \
    echo '}' >> /etc/nginx/sites-available/simtax

# Enable the site
RUN ln -sf /etc/nginx/sites-available/simtax /etc/nginx/sites-enabled/ && \
    rm -f /etc/nginx/sites-enabled/default

# Create supervisor configuration (using echo commands)
RUN echo '[supervisord]' > /etc/supervisor/conf.d/supervisord.conf && \
    echo 'nodaemon=true' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'user=root' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'logfile=/dev/stdout' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'logfile_maxbytes=0' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo '' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo '[program:nginx]' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'command=/usr/sbin/nginx -g "daemon off;"' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'autostart=true' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'autorestart=true' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'stdout_logfile=/dev/stdout' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'stdout_logfile_maxbytes=0' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'stderr_logfile=/dev/stderr' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'stderr_logfile_maxbytes=0' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo '' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo '[program:mockserver]' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'command=python /app/mockserver.py' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'user=appuser' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'autostart=true' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'autorestart=true' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'stdout_logfile=/dev/stdout' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'stdout_logfile_maxbytes=0' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'stderr_logfile=/dev/stderr' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'stderr_logfile_maxbytes=0' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'environment=PORT="5000"' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo '' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo '[program:webinterface]' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'command=python /app/web_interface.py' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'user=appuser' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'autostart=true' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'autorestart=true' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'stdout_logfile=/dev/stdout' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'stdout_logfile_maxbytes=0' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'stderr_logfile=/dev/stderr' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'stderr_logfile_maxbytes=0' >> /etc/supervisor/conf.d/supervisord.conf && \
    echo 'environment=PORT="5001"' >> /etc/supervisor/conf.d/supervisord.conf

# Create entrypoint script
RUN echo '#!/bin/bash' > /docker-entrypoint.sh && \
    echo 'set -e' >> /docker-entrypoint.sh && \
    echo '' >> /docker-entrypoint.sh && \
    echo '# Replace the port in nginx config if PORT environment variable is different' >> /docker-entrypoint.sh && \
    echo 'if [ ! -z "$PORT" ] && [ "$PORT" != "8080" ]; then' >> /docker-entrypoint.sh && \
    echo '    sed -i "s/listen 8080/listen $PORT/" /etc/nginx/sites-available/simtax' >> /docker-entrypoint.sh && \
    echo 'fi' >> /docker-entrypoint.sh && \
    echo '' >> /docker-entrypoint.sh && \
    echo '# Start supervisord' >> /docker-entrypoint.sh && \
    echo 'exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf' >> /docker-entrypoint.sh

RUN chmod +x /docker-entrypoint.sh

# Ensure proper permissions for nginx
RUN touch /var/log/nginx/access.log /var/log/nginx/error.log && \
    chown -R appuser:appgroup /var/log/nginx /var/lib/nginx /run/nginx.pid 2>/dev/null || true

# Expose the port
EXPOSE 8080

# Use the custom entrypoint
ENTRYPOINT ["/docker-entrypoint.sh"]
