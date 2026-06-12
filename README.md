# 🌱 WaterWiseAg – Smart Irrigation & Water Requirement Prediction System

## 📌 Overview

WaterWiseAg is an AI-powered smart irrigation decision support system designed to help farmers optimize water usage and improve agricultural productivity. The system predicts crop water requirements using machine learning by analyzing environmental conditions and farm-specific inputs.

By combining weather information, soil characteristics, crop details, and land area, WaterWiseAg provides accurate irrigation recommendations that support sustainable farming and water conservation.

---

## 🚀 Features

### 🌾 Water Requirement Prediction

Predicts the amount of water required for crops based on:

* Land Area
* Soil Type
* Crop Type
* Crop Growth Stage
* Season
* Temperature
* Humidity
* Rainfall
* Wind Speed

### 🌦 Real-Time Weather Integration

Fetches live weather data using the OpenWeather API to improve prediction accuracy.

### 📊 Interactive Dashboard

Provides a user-friendly interface for entering farm details and viewing predictions.

### 💡 Smart Recommendations

Generates actionable irrigation recommendations based on predicted water requirements.

### 📄 PDF Report Generation

Allows users to download prediction results and recommendations as a PDF report.

### 🌐 Web-Based Accessibility

Accessible through a Streamlit web application from any device with an internet connection.

---

## 🏗 System Architecture

Frontend (Streamlit)

↓

Backend (Flask REST API)

↓

Machine Learning Model (Scikit-Learn)

↓

Prediction & Recommendations

↓

PDF Report Generation

---

## 🛠 Technology Stack

### Frontend

* Streamlit

### Backend

* Flask
* Flask-CORS

### Machine Learning

* Scikit-Learn
* Joblib
* Pandas
* NumPy

### External Services

* OpenWeather API

### Deployment

* Streamlit Community Cloud (Frontend)
* Render (Backend)

---

## 📂 Project Structure

```text
WATERWISEAG
│
├── backend
│   ├── app.py
│   ├── .env
│   └── .env.example
│
├── frontend
│   └── front.py
│
├── models
│   ├── model.pkl
│   ├── train_model.py
│   └── smart_water_prediction.csv
│
├── requirements.txt
└── .gitignore
```

## 🔄 Workflow

1. User enters farm and environmental details.
2. Streamlit frontend sends data to Flask API.
3. Flask processes the request.
4. Machine Learning model predicts water requirement.
5. Prediction is returned to the frontend.
6. Recommendations are generated.
7. User can download a PDF report.

---

## 🎯 Objectives

* Promote efficient water utilization.
* Support data-driven irrigation decisions.
* Reduce water wastage in agriculture.
* Improve crop health and productivity.
* Assist farmers with real-time environmental insights.

---

## 📈 Future Enhancements

* Multilingual support (English, Hindi, Tamil, etc.)
* Mobile application development
* IoT sensor integration
* Satellite and remote sensing data integration
* Crop disease prediction
* Advanced analytics dashboard

---

## 👩‍💻 Developed By

**Vijayashree B**

AI & Machine Learning Enthusiast | Full Stack Developer | Data Science Learner

---

## 📜 License

This project is developed for educational, research, and demonstration purposes.
