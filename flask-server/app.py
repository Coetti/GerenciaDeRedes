import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from routes.audio_routes import audio_bp
import config

app = Flask(__name__)
app.register_blueprint(audio_bp)

if __name__ == "__main__":
    app.run(debug=True)
