from flask import Flask
from flask_cors import CORS
import joblib
import os

app = Flask(__name__)
CORS(app)

# =========================
# Load trained model safely
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "model.pkl")

ml_model = joblib.load(MODEL_PATH)

# =========================
# Routes
# =========================
@app.route("/")
def home():
    return "Backend is running! Model loaded successfully."

# =========================
# Run server
# =========================
if __name__ == "__main__":
    app.run(debug=True)