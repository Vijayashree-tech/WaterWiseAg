from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import joblib
import pandas as pd
import os
from dotenv import load_dotenv
import requests

# ------------------------
# Load environment variables
# ------------------------
load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

app = Flask(__name__)
CORS(app)

# ------------------------
# Load trained model (JOBLIB)
# ------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "model.pkl")

ml_model = joblib.load(MODEL_PATH)

# ------------------------
# Home Route
# ------------------------
@app.route("/")
def home():
    return "Backend is running!"


@app.route("/predict", methods=["POST"])
def predict():
    print("PREDICT ROUTE HIT")
    data = request.get_json()

    try:
        required_fields = [
            "land_area",
            "temperature",
            "humidity",
            "rainfall",
            "wind_speed",
            "soil_type",
            "crop_type",
            "crop_stage",
            "season",
        ]

        for field in required_fields:
            if field not in data:
                return jsonify({
                    "error": f"Missing field: {field}"
                }), 400

        # ----------------------------
        # Prepare Model Input
        # Column names must match exactly what the model was trained on
        # ----------------------------
        features_dict = {
            "Land_Area_acres": float(data["land_area"]),
            "Temperature_C": float(data["temperature"]),
            "Humidity_pct": float(data["humidity"]),
            "Rainfall_mm": float(data["rainfall"]),
            "WindSpeed_kmph": float(data["wind_speed"]),
            "Soil_Type": data["soil_type"],
            "Crop_Type": data["crop_type"],
            "Crop_Stage": data["crop_stage"],
            "Season": data["season"],
        }

        features_df = pd.DataFrame([features_dict])

        # ----------------------------
        # ML Prediction
        # Model is trained on a realistic litres/day target
        # (rescaled to ~15,000-60,000 L/acre/day; see train_model.py)
        # ----------------------------
        prediction = float(ml_model.predict(features_df)[0])
        water_required_liters = round(max(0.0, prediction), 1)

        # ----------------------------
        # Irrigation Level
        # Thresholds set from the rescaled training data's
        # 33rd / 66th percentiles so Low/Medium/High are each
        # genuinely represented, not collapsed into one bucket.
        # ----------------------------
        if water_required_liters < 90000:
            irrigation_level = "Low"
            confidence = 85
        elif water_required_liters < 180000:
            irrigation_level = "Medium"
            confidence = 90
        else:
            irrigation_level = "High"
            confidence = 95

        # ----------------------------
        # Explanation Engine
        # ----------------------------
        reasons = []

        temp = float(data["temperature"])
        humidity = float(data["humidity"])
        rainfall = float(data["rainfall"])
        wind = float(data["wind_speed"])

        if temp > 35:
            reasons.append("High temperature increases crop water demand")

        if rainfall < 5:
            reasons.append("Low rainfall detected")

        if humidity < 50:
            reasons.append("Low humidity increases evaporation")

        if wind > 15:
            reasons.append("High wind speed may increase water loss")

        if irrigation_level == "High":
            reasons.append("Crop requires higher irrigation under current conditions")

        if not reasons:
            reasons.append("Weather conditions are favorable for crop growth")

        # ----------------------------
        # Response
        # ----------------------------
        return jsonify({
            "water_required_liters": water_required_liters,
            "irrigation_level": irrigation_level,
            "confidence": confidence,
            "weather_used": {
                "temperature": temp,
                "humidity": humidity,
                "rainfall": rainfall,
                "wind_speed_kmph": wind,
            },
            "explanation": reasons,
        }), 200

    except Exception as e:
        return jsonify({
            "error": f"Prediction failed: {str(e)}"
        }), 500


# ------------------------
# Report Route
# ------------------------
@app.route("/report", methods=["GET"])
def generate_report():
    report_path = os.path.join(BASE_DIR, "report.pdf")

    if not os.path.exists(report_path):
        return jsonify({"error": "Report not found"}), 404

    return send_file(report_path, as_attachment=True)


# ------------------------
# Weather Route
# ------------------------
@app.route("/weather/<city>")
def weather(city):
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        )

        response = requests.get(url, timeout=5)

        return jsonify(response.json())

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ------------------------
# Run Flask App
# ------------------------
if __name__ == "__main__":
    app.run(debug=True)
