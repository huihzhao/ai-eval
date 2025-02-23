# AlphaSight Server

Flask-based API server for project analysis.

## Local Development

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create .env file:
```bash
PORT=3000
GEMINI_API_KEY=your_key_here
```

4. Run server:
```bash
python main.py
```

## Docker Deployment

### Using Docker Compose (Development)
```bash
docker-compose up --build
```

### Production Deployment
```bash
docker build -t alphasight-server .
docker run -d -p 3000:3000 --env-file .env alphasight-server
```

## SSL Configuration

1. Create SSL directory and generate certificates:
```bash
mkdir ssl
cd ssl
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
cd ..
```

2. Update .env file to include SSL settings:
```bash
PORT=3443
GEMINI_API_KEY=your_key_here
```

3. For development with SSL:
```bash
python main.py
```

4. For Docker deployment with SSL, mount certificates:
```bash
docker run -d -p 3443:3443 \
  --env-file .env \
  -v $(pwd)/ssl:/app/ssl \
  alphasight-server
```

Note: 
- The server automatically detects SSL certificates in the `ssl` directory
- Default HTTPS port is 3443
- In production, use properly signed certificates from a trusted CA
- If certificates are missing, the server will fall back to HTTP mode

## API Endpoints

- POST /api/project/analyze - Analyze project
  - Request: Project details (name, website, description, etc.)
  - Response: Project analysis and scores
