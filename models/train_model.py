import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# =========================
# 1. Load dataset
# =========================
df = pd.read_csv("smart_water_predictor_20000_dataset.csv")

# =========================
# 2. Split features & target
# =========================
X = df.drop("Water_Required_Litres", axis=1)
y = df["Water_Required_Litres"]

# =========================
# 3. Categorical columns
# =========================
categorical_cols = ["Soil_Type", "Crop_Type", "Crop_Stage", "Season"]

# =========================
# 4. Preprocessing (OPTIMIZED)
# =========================
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(
            handle_unknown="ignore",
            sparse_output=True,
            max_categories=10   # prevents explosion of features
        ), categorical_cols)
    ],
    remainder="passthrough"
)

# =========================
# 5. Model (REDUCED SIZE)
# =========================
model = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(
        n_estimators=80,   # reduced from 200
        max_depth=12,      # prevents huge trees
        random_state=42,
        n_jobs=-1
    ))
])

# =========================
# 6. Train-test split
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# 7. Train model
# =========================
model.fit(X_train, y_train)

# =========================
# 8. Predictions
# =========================
y_pred = model.predict(X_test)

# =========================
# 9. Evaluation
# =========================
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\nModel Performance:")
print("MAE:", mae)
print("RMSE:", rmse)
print("R2 Score:", r2)

# =========================
# 10. Save model (COMPRESSED)
# =========================
joblib.dump(model, "model.pkl", compress=3)

print("\nModel saved as model.pkl (compressed)")