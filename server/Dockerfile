FROM python:3.12-slim

WORKDIR /app/server

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy server requirements first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy server code
COPY . .

# Set environment variables
ENV PORT=3000
ENV PYTHONPATH=/app/server

# Expose the port
EXPOSE 3000

# Run the application
CMD ["python", "main.py"]
