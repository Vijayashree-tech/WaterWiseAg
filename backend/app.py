from flask import Flask
from flask_cors import CORS
import pickle
import os

app = Flask(__name__)
CORS(app)

# Load trained model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "model.pkl")

with open(MODEL_PATH, "rb") as f:
    ml_model = pickle.load(f)

@app.route("/")
def home():
    return "Backend is running! Model loaded successfully."

if __name__ == "__main__":
    app.run(debug=True)