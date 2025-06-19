import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from flask import Flask
from flask_cors import CORS
from routes.audio_routes import audio_bp

app = Flask(__name__)
CORS(app)
app.register_blueprint(audio_bp)

if __name__ == "__main__":
    app.run(debug=True)
