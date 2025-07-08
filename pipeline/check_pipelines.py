import json
import os
import joblib
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

df = pd.read_csv(r"C:\Users\USUARIO\Downloads\cleaned_titanic.csv")

X = df[["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked"]]
y = df["Survived"]

# Split and train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
print(model.score(X_train, y_train))

y_pred = model.predict(X_test)

# Assume you have y_test and y_pred from your evaluation
accuracy = accuracy_score(y_test, y_pred)

# Save metrics
metrics = {
    "regression_metrics": {
        "accuracy": {
            "value": accuracy,
            "standard_deviation": 0.0  # optional
        }
    }
}

print(os.makedirs("/opt/ml/output/metrics", exist_ok=True))

with open("metrics.json", "w") as f:
    json.dump(metrics, f)

# Save model to /opt/ml/model (SageMaker expects this path)
joblib.dump(model, "model.joblib")