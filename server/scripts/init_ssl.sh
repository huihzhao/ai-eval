#!/bin/bash

SSL_DIR="ssl"
CERT_FILE="$SSL_DIR/cert.pem"
KEY_FILE="$SSL_DIR/key.pem"

# Create SSL directory if it doesn't exist
mkdir -p $SSL_DIR

# Generate self-signed certificate and private key
openssl req -x509 \
    -newkey rsa:4096 \
    -nodes \
    -out $CERT_FILE \
    -keyout $KEY_FILE \
    -days 365 \
    -subj "/CN=localhost" \
    -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"

# Set proper permissions
chmod 600 $KEY_FILE
chmod 644 $CERT_FILE

echo "SSL certificates generated successfully:"
echo "  - Certificate: $CERT_FILE"
echo "  - Private key: $KEY_FILE"