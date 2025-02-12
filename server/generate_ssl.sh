#!/bin/bash

# Create SSL directory if it doesn't exist
mkdir -p ssl

# Generate SSL certificate and key
openssl req -x509 -newkey rsa:4096 -nodes -out ssl/cert.pem -keyout ssl/key.pem -days 365 -subj "/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=localhost"

echo "Self-signed SSL certificate generated in the ssl directory."
