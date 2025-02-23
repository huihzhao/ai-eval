from quart import Quart
from quart_cors import cors
from routers import project, auth
from dotenv import load_dotenv
import os
import traceback
import ssl
import asyncio

load_dotenv()

app = Quart(__name__)
app = cors(app)

# Enable debug mode for more detailed errors
app.debug = True

# Register blueprints
app.register_blueprint(auth.blueprint, url_prefix='/api/auth')
app.register_blueprint(project.blueprint, url_prefix='/api/project')

@app.errorhandler(Exception)
async def handle_exception(e):
    print(f"Unhandled exception: {str(e)}")
    print(traceback.format_exc())
    return {"error": "An unexpected error occurred", "details": str(e)}, 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3443))
    ssl_enabled = os.getenv("ENABLE_SSL", "true").lower() == "true"
    
    if ssl_enabled:
        cert_path = os.path.join(os.path.dirname(__file__), "ssl/cert.pem")
        key_path = os.path.join(os.path.dirname(__file__), "ssl/key.pem")
        
        print(f"Starting HTTPS server on port {port}")
        print(f"Using certificates at:")
        print(f"  - Cert: {cert_path}")
        print(f"  - Key: {key_path}")
        
        app.run(
            host="0.0.0.0",
            port=port,
            certfile=cert_path,
            keyfile=key_path,
            debug=True
        )
    else:
        print(f"Starting HTTP server on port {port}")
        app.run(host="0.0.0.0", port=port, debug=True)
