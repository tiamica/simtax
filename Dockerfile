FROM python:3.11-slim

WORKDIR /app

# Install nginx
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

# Copy and install Python deps
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy all code
COPY . .

# Configure nginx (using simple echo commands)
RUN echo 'server {' > /etc/nginx/sites-enabled/default && \
    echo '    listen 8080;' >> /etc/nginx/sites-enabled/default && \
    echo '    location ~ ^/(send|status|calculate-tax) {' >> /etc/nginx/sites-enabled/default && \
    echo '        proxy_pass http://127.0.0.1:5000;' >> /etc/nginx/sites-enabled/default && \
    echo '    }' >> /etc/nginx/sites-enabled/default && \
    echo '    location / {' >> /etc/nginx/sites-enabled/default && \
    echo '        proxy_pass http://127.0.0.1:5001;' >> /etc/nginx/sites-enabled/default && \
    echo '    }' >> /etc/nginx/sites-enabled/default && \
    echo '}' >> /etc/nginx/sites-enabled/default

# Simple launcher script
RUN echo '#!/bin/bash' > /start.sh && \
    echo 'python mockserver.py &' >> /start.sh && \
    echo 'python web_interface.py &' >> /start.sh && \
    echo 'nginx -g "daemon off;"' >> /start.sh && \
    chmod +x /start.sh

EXPOSE 8080

CMD ["/start.sh"]
