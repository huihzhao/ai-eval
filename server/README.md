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

## API Endpoints

- POST /api/project/analyze - Analyze project
  - Request: Project details (name, website, description, etc.)
  - Response: Project analysis and scores
