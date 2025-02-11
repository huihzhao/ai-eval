from flask import Flask
from flask_cors import CORS
from routers import project
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(project.blueprint, url_prefix='/api/project')

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=True)
