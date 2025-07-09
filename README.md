# 🚢 Titanic Survival Prediction – SageMaker MLOps Pipeline

This project demonstrates a complete MLOps workflow using AWS SageMaker to train, evaluate, register, and deploy a machine learning model for predicting Titanic passenger survival.

---

## 🧠 Problem Statement

Predict whether a passenger survived the Titanic disaster using features such as class, age, fare, and more. The model is trained and deployed using a robust, automated pipeline on AWS SageMaker.

---

## 📁 Project Structure

```

.
├── scripts/
│   ├── train.py                # Training script used by SageMaker
│   ├── inference.py            # Entry point for deployed model
│   ├── model\_utils.py          # Wrapper for inference preprocessing
│   └── **init**.py             # To make the scripts folder a module
├── deployment/
│   ├── deploy\_endpoint.py      # Script to deploy model as endpoint
│   └── invoke\_endpoint.py      # Script to test endpoint prediction
├── pipeline/
│   └── pipeline\_definition.py  # Defines the SageMaker pipeline
├── processed\_data/             # Input data for the pipeline
├── raw\_data/                   # Original Titanic dataset
├── README.md
└── requirements.txt

````

---

## 🔧 Technologies Used

- **AWS SageMaker**: Pipelines, Training, Model Registry, Endpoints
- **scikit-learn**: Model training
- **SageMaker Python SDK**
- **Boto3**: For deployment and endpoint invocation
- **joblib**: Model serialization

---

## ⚙️ Pipeline Overview

### ✅ Steps

1. **Preprocessing**
   - Raw CSV → Cleaned features saved to S3
2. **Training**
   - Logistic regression using `scikit-learn`
   - Saves model as `model.joblib`
   - Calculates and logs metrics (accuracy)
3. **Model Registration**
   - Registers model in SageMaker Model Registry with metrics
4. **Deployment**
   - Deploys the approved model as a real-time endpoint

---

## 📊 Metrics

- Model Accuracy: **~75.5%**
- Stored in S3 as `metrics.json`
- Registered in SageMaker Model Registry

---

## 🚀 Endpoint Invocation

Use the deployed endpoint to make real-time predictions. Example:

```bash
python deployment/invoke_endpoint.py
````

Sample input:

```csv
3,1,22.0,0,0,7.25,0
```

Prediction Output:

```text
Prediction: [1]
```

---

## ✅ Skills Demonstrated

* ✅ End-to-end MLOps pipeline design
* ✅ Real-time endpoint deployment using Boto3
* ✅ Custom inference wrappers and model serialization
* ✅ SageMaker Pipeline & Model Registry integration
* ✅ Error debugging and AWS log analysis

---

## 📝 How to Run This Project

1. Upload data to S3
2. Run the pipeline:

```bash
python pipeline/pipeline_definition.py
```

3. Deploy and test the endpoint:

```bash
python deployment/deploy_endpoint.py
python deployment/invoke_endpoint.py
```

---

## 📌 Notes

* The pipeline automatically registers and approves the model.
* The custom wrapper ensures all predictions work even with a single input row.
* Metrics are embedded in the model package for auditability.

---

## 📬 Contact

Created by **\[Johan Zuluaga]**.
For questions, feel free to reach out via \[johandzuluaga@gmail.com].

---

