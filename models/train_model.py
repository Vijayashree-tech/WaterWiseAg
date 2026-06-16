import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

RAW_PATH = "smart_water_predictor_20000_dataset_rescaled.csv"

REALISTIC_MIN_PER_ACRE = 15000.0   # litres/acre/day
REALISTIC_MAX_PER_ACRE = 60000.0   # litres/acre/day

# =========================
# 1. Load dataset
# =========================
df = pd.read_csv(RAW_PATH)

# =========================
# 2. Rescale target to a realistic litres/day range
# =========================
per_acre_raw = df["Water_Required_Litres"] / df["Land_Area_acres"]

old_min, old_max = per_acre_raw.min(), per_acre_raw.max()
per_acre_scaled = REALISTIC_MIN_PER_ACRE + (per_acre_raw - old_min) / (old_max - old_min) * (
    REALISTIC_MAX_PER_ACRE - REALISTIC_MIN_PER_ACRE
)

df["Water_Required_Litres"] = per_acre_scaled * df["Land_Area_acres"]

print("Rescaled target stats (litres/day, whole farm):")
print(df["Water_Required_Litres"].describe())
print()

# =========================
# 3. Split features & target
# =========================
X = df.drop("Water_Required_Litres", axis=1)
y = df["Water_Required_Litres"]

# =========================
# 4. Categorical columns
# =========================
categorical_cols = ["Soil_Type", "Crop_Type", "Crop_Stage", "Season"]

# =========================
# 5. Preprocessing
# =========================
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=True), categorical_cols)
    ],
    remainder="passthrough",
)

# =========================
# 6. Model
# =========================
model = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(
        n_estimators=200,
        max_depth=16,
        min_samples_leaf=3,
        random_state=42,
        n_jobs=-1,
    )),
])

# =========================
# 7. Train-test split
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# 8. Train model
# =========================
model.fit(X_train, y_train)

# =========================
# 9. Predictions & evaluation
# =========================
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("Model Performance (on rescaled, realistic litres/day target):")
print("MAE :", round(mae, 2), "litres/day")
print("RMSE:", round(rmse, 2), "litres/day")
print("R2  :", round(r2, 4))
print()

# Sanity check: predictions should clearly vary across different inputs
sample = X_test.iloc[:8].copy()
sample["Predicted_Litres"] = model.predict(sample)
print("Sample predictions (sanity check for variation):")
print(sample[["Land_Area_acres", "Crop_Type", "Crop_Stage", "Season", "Predicted_Litres"]])

# =========================
# 10. Save model
# =========================
joblib.dump(model, "model.pkl", compress=3)
print("\nModel saved as model.pkl")
