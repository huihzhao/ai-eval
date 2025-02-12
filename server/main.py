from flask import Flask, jsonify
from flask_cors import CORS
from routers import project, auth
from dotenv import load_dotenv
import os
import traceback
import ssl

load_dotenv()

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(auth.blueprint, url_prefix='/api/auth')
app.register_blueprint(project.blueprint, url_prefix='/api/project')

@app.errorhandler(Exception)
def handle_exception(e):
    print(f"Unhandled exception: {str(e)}")
    print(traceback.format_exc())
    return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3443))  # Default to 3443 for HTTPS
    ssl_dir = os.path.join(os.path.dirname(__file__), 'ssl')
    cert_path = os.path.join(ssl_dir, 'cert.pem')
    key_path = os.path.join(ssl_dir, 'key.pem')
    
    if os.path.exists(cert_path) and os.path.exists(key_path):
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(certfile=cert_path, keyfile=key_path)
        print(f"Starting server with HTTPS on port {port}")
        app.run(host="0.0.0.0", port=port, ssl_context=ssl_context, debug=True)
    else:
        print(f"SSL certificates not found. Starting server without HTTPS on port {port}")
        app.run(host="0.0.0.0", port=port, debug=True)
