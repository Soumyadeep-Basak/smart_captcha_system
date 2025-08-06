# 🚀 Smart Captcha System - Deployment Guide

This guide covers deploying the Smart Captcha System in various environments, from development to production.

## 📋 Prerequisites

### System Requirements

**Minimum Requirements:**
- CPU: 2 cores
- RAM: 4GB
- Storage: 10GB
- Network: 100Mbps

**Recommended for Production:**
- CPU: 4+ cores
- RAM: 8GB+
- Storage: 50GB+ SSD
- Network: 1Gbps

### Software Dependencies

- **Python**: 3.8+ (3.9+ recommended)
- **Node.js**: 16+ (18+ recommended)
- **Git**: Latest version
- **Docker**: 20.10+ (optional but recommended)
- **Nginx**: 1.18+ (for production)

## 🏠 Local Development

### Quick Start

1. **Clone Repository**
```bash
git clone https://github.com/your-org/smart-captcha-system.git
cd smart-captcha-system
```

2. **Backend Setup**
```bash
cd backend/api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

3. **Frontend Setup**
```bash
cd frontend
npm install
npm run dev
```

### Environment Variables

Create `.env` files for local development:

**Backend (.env):**
```env
FLASK_ENV=development
DEBUG=True
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:3000
ML_MODEL_PATH=./models/
PREDICTIONS_LOG_PATH=./logs/predictions/
DETECTION_THRESHOLD=0.4
HONEYPOT_WEIGHT=0.45
ML_WEIGHT=0.35
FINGERPRINT_WEIGHT=0.20
```

**Frontend (.env.local):**
```env
NEXT_PUBLIC_API_URL=http://localhost:5000
NEXT_PUBLIC_ENABLE_HONEYPOTS=true
NEXT_PUBLIC_DEBUG_MODE=true
```

## 🐳 Docker Deployment

### Docker Compose (Recommended)

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DEBUG=False
      - CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
    volumes:
      - ./backend/logs:/app/logs
      - ./backend/models:/app/models
    networks:
      - smart-captcha-network
    restart: unless-stopped

  frontend:
    build:
      context: .
      dockerfile: frontend/Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:5000
      - NODE_ENV=production
    depends_on:
      - backend
    networks:
      - smart-captcha-network
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
    networks:
      - smart-captcha-network
    restart: unless-stopped

networks:
  smart-captcha-network:
    driver: bridge
```

### Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

### Individual Docker Images

**Backend Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ .

# Create necessary directories
RUN mkdir -p logs/predictions models

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

# Run application
CMD ["python", "api/app.py"]
```

**Frontend Dockerfile:**
```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY frontend/package*.json ./
RUN npm ci --only=production

# Copy source code and build
COPY frontend/ .
RUN npm run build

FROM node:18-alpine AS runner

WORKDIR /app

# Copy built application
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

# Create non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

USER nextjs

EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

CMD ["npm", "start"]
```

## ☁️ Cloud Deployment

### AWS Deployment

#### EC2 Instance Setup

1. **Launch EC2 Instance**
```bash
# t3.medium or larger recommended
# Ubuntu 20.04 LTS
# Security groups: 22 (SSH), 80 (HTTP), 443 (HTTPS)
```

2. **Install Dependencies**
```bash
sudo apt update
sudo apt install -y python3 python3-pip nodejs npm nginx certbot python3-certbot-nginx git

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

3. **Deploy Application**
```bash
git clone https://github.com/your-org/smart-captcha-system.git
cd smart-captcha-system

# Set production environment variables
cp .env.example .env
# Edit .env with production values

# Deploy with Docker Compose
docker-compose -f docker-compose.prod.yml up -d
```

#### ECS Deployment

**task-definition.json:**
```json
{
  "family": "smart-captcha-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::ACCOUNT:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "your-account.dkr.ecr.region.amazonaws.com/smart-captcha-backend:latest",
      "portMappings": [
        {
          "containerPort": 5000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "FLASK_ENV", "value": "production"},
        {"name": "DEBUG", "value": "False"}
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/smart-captcha",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "backend"
        }
      }
    }
  ]
}
```

### Google Cloud Platform

#### Cloud Run Deployment

1. **Build and Push Images**
```bash
# Configure gcloud
gcloud auth configure-docker

# Build images
docker build -t gcr.io/PROJECT_ID/smart-captcha-backend backend/
docker build -t gcr.io/PROJECT_ID/smart-captcha-frontend frontend/

# Push images
docker push gcr.io/PROJECT_ID/smart-captcha-backend
docker push gcr.io/PROJECT_ID/smart-captcha-frontend
```

2. **Deploy to Cloud Run**
```bash
# Deploy backend
gcloud run deploy smart-captcha-backend \
  --image gcr.io/PROJECT_ID/smart-captcha-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2

# Deploy frontend
gcloud run deploy smart-captcha-frontend \
  --image gcr.io/PROJECT_ID/smart-captcha-frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars NEXT_PUBLIC_API_URL=https://backend-url
```

### Microsoft Azure

#### Container Instances

```bash
# Create resource group
az group create --name smart-captcha-rg --location eastus

# Deploy backend
az container create \
  --resource-group smart-captcha-rg \
  --name smart-captcha-backend \
  --image your-registry/smart-captcha-backend:latest \
  --dns-name-label smart-captcha-api \
  --ports 5000 \
  --cpu 2 \
  --memory 4 \
  --environment-variables FLASK_ENV=production

# Deploy frontend
az container create \
  --resource-group smart-captcha-rg \
  --name smart-captcha-frontend \
  --image your-registry/smart-captcha-frontend:latest \
  --dns-name-label smart-captcha-app \
  --ports 3000 \
  --cpu 1 \
  --memory 2 \
  --environment-variables NEXT_PUBLIC_API_URL=https://smart-captcha-api.eastus.azurecontainer.io:5000
```

## 🌐 Production Configuration

### Nginx Configuration

**nginx.conf:**
```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:5000;
    }

    upstream frontend {
        server frontend:3000;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;

    server {
        listen 80;
        server_name yourdomain.com www.yourdomain.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name yourdomain.com www.yourdomain.com;

        # SSL Configuration
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        # Security Headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

        # Frontend
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # API
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            
            proxy_pass http://backend/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Health checks
        location /health {
            proxy_pass http://backend/health;
            access_log off;
        }
    }
}
```

### SSL Certificate Setup

#### Let's Encrypt (Certbot)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

#### Manual Certificate

```bash
# Generate private key
openssl genrsa -out private.key 2048

# Generate certificate signing request
openssl req -new -key private.key -out cert.csr

# Generate self-signed certificate (for testing)
openssl x509 -req -days 365 -in cert.csr -signkey private.key -out cert.crt
```

### Environment Configuration

**Production .env:**
```env
# Backend Configuration
FLASK_ENV=production
DEBUG=False
LOG_LEVEL=WARNING
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@host/db

# Security
CORS_ORIGINS=https://yourdomain.com
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECURE_SSL_REDIRECT=True

# Detection Settings
DETECTION_THRESHOLD=0.4
HONEYPOT_WEIGHT=0.45
ML_WEIGHT=0.35
FINGERPRINT_WEIGHT=0.20

# Rate Limiting
RATE_LIMIT_PER_MINUTE=100
RATE_LIMIT_BURST=10

# Monitoring
SENTRY_DSN=your-sentry-dsn
LOG_TO_FILE=True
LOG_FILE_PATH=/app/logs/app.log
```

## 📊 Monitoring and Logging

### Application Monitoring

#### Prometheus + Grafana

**docker-compose.monitoring.yml:**
```yaml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'

  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-storage:/var/lib/grafana
      - ./monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./monitoring/grafana/datasources:/etc/grafana/provisioning/datasources

volumes:
  grafana-storage:
```

#### Health Checks

```python
# Add to backend/api/app.py
@app.route('/health')
def health_check():
    """Comprehensive health check"""
    checks = {
        'api': 'healthy',
        'database': check_database(),
        'ml_models': check_ml_models(),
        'disk_space': check_disk_space(),
        'memory_usage': check_memory_usage()
    }
    
    status = 'healthy' if all(v == 'healthy' for v in checks.values()) else 'unhealthy'
    
    return jsonify({
        'status': status,
        'timestamp': datetime.utcnow().isoformat(),
        'checks': checks
    }), 200 if status == 'healthy' else 503
```

### Logging Configuration

**Production Logging Setup:**
```python
import logging
from logging.handlers import RotatingFileHandler
import os

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = RotatingFileHandler(
        'logs/smart_captcha.log', 
        maxBytes=10240000, 
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    
    app.logger.setLevel(logging.INFO)
    app.logger.info('Smart Captcha System startup')
```

## 🔧 Scaling and Performance

### Horizontal Scaling

#### Load Balancer Configuration

```yaml
# docker-compose.scale.yml
version: '3.8'

services:
  backend:
    build: backend/
    deploy:
      replicas: 3
    environment:
      - FLASK_ENV=production
    networks:
      - app-network

  load-balancer:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/load-balancer.conf:/etc/nginx/nginx.conf
    depends_on:
      - backend
    networks:
      - app-network
```

#### Auto-scaling (Kubernetes)

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: smart-captcha-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: smart-captcha-backend
  template:
    metadata:
      labels:
        app: smart-captcha-backend
    spec:
      containers:
      - name: backend
        image: smart-captcha-backend:latest
        ports:
        - containerPort: 5000
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: smart-captcha-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: smart-captcha-backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Performance Optimization

#### Caching

```python
# Add Redis caching
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0',
    'CACHE_DEFAULT_TIMEOUT': 300
})

@app.route('/predict', methods=['POST'])
@cache.memoize(timeout=60)  # Cache predictions for 1 minute
def predict():
    # Implementation
    pass
```

#### Database Optimization

```python
# Connection pooling
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=30,
    pool_recycle=3600
)
```

## 🚨 Troubleshooting

### Common Issues

1. **High Memory Usage**
```bash
# Monitor memory
docker stats

# Reduce model memory footprint
# Edit backend/api/modules/ml_model.py
# Implement model quantization or pruning
```

2. **Slow API Response**
```bash
# Check logs
docker-compose logs backend

# Profile API performance
# Add timing decorators to functions
```

3. **SSL Certificate Issues**
```bash
# Check certificate validity
openssl x509 -in cert.pem -text -noout

# Verify Nginx configuration
nginx -t
```

4. **High CPU Usage**
```bash
# Monitor CPU
top -p $(pgrep -f "python app.py")

# Optimize ML models
# Consider model caching and batch processing
```

### Log Analysis

```bash
# Search for errors
grep ERROR logs/smart_captcha.log

# Monitor real-time logs
tail -f logs/smart_captcha.log

# Analyze performance
grep "processing_time" logs/smart_captcha.log | awk '{print $5}' | sort -n
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt](https://letsencrypt.org/)
- [AWS ECS Guide](https://docs.aws.amazon.com/ecs/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)

---

Need help with deployment? Check our [troubleshooting guide](TROUBLESHOOTING.md) or open an issue on GitHub.
