import argparse
import pandas as pd
import joblib
import os
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', type=str, default='/opt/ml/input/data/train')
    parser.add_argument('--model-dir', type=str, default='/opt/ml/model')
    args = parser.parse_args()

    # Read cleaned file
    df = pd.read_csv(os.path.join(args.train, "cleaned_titanic.csv"))

    # Split features and target
    X = df[["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked"]]
    y = df["Survived"]

    # Split and train
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    # Save model to /opt/ml/model (SageMaker expects this path)
    joblib.dump(model, "/opt/ml/model/model.joblib")
