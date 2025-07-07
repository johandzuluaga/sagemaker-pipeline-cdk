import pandas as pd
import os

INPUT_PATH = "/opt/ml/processing/input/titanic.csv"
OUTPUT_PATH = "/opt/ml/processing/output/train/cleaned_titanic.csv"

def preprocess():
    # Load data
    df = pd.read_csv(INPUT_PATH)

    # Drop columns not useful for modeling
    df = df.drop(columns=["Name", "Ticket", "Cabin"])

    # Drop rows with missing values (basic cleaning)
    df = df.dropna()

    # Encode categorical variables
    df["Sex"] = df["Sex"].map({"male": 0, "female": 1})
    df["Embarked"] = df["Embarked"].map({"C": 0, "Q": 1, "S": 2})

    # Save processed dataset
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"✅ Preprocessing complete. Saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    preprocess()
