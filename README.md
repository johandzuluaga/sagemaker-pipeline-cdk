# SageMaker MLOps Pipeline with AWS CDK and SDK

This project showcases a complete MLOps pipeline on AWS SageMaker, with infrastructure defined using the AWS CDK and programmatic interactions managed through the AWS SDK for Python (boto3). The pipeline automates the data preparation, training, evaluation, registration, and deployment of ML models using best practices for reproducibility, traceability, and scalability.

---

## 📁 Project Structure

```

.
├── deployment/
│   ├── deploy_endpoint.py        # Script to deploy model as endpoint
│   └── invoke_endpoint.py        # Script to test endpoint prediction
├── pipeline/
│   └── pipeline_definition.py    # Defines the SageMaker pipeline
├── sage_maker_test/
│   └── sage_maker_test_stack.py  # Defines the CDK stack
│   └── __init__.py               # To make the folder a module
├── scripts/
│   ├── train.py                  # Training script used by SageMaker
│   ├── inference.py              # Entry point for deployed model
│   ├── model_utils.py            # Wrapper for inference preprocessing
│   └── __init__.py               # To make the scripts folder a module
├── README.md
└── requirements.txt

````

---

## 🧰 Tools & Technologies

| Tool/Service         | Purpose                                         |
| -------------------- | ----------------------------------------------- |
| **AWS SageMaker**    | Train, evaluate, register, and deploy ML models |
| **AWS CDK (Python)** | Define and deploy infrastructure as code        |
| **boto3 (AWS SDK)**  | Automate SageMaker operations programmatically  |
| **S3**               | Store data, model artifacts, and metrics        |
| **sklearn**          | (Example only) ML model used for demonstration  |

---

## 🧱 Architecture Overview

The solution is composed of two parts:

1. **Infrastructure (CDK)**:

   * Sets up SageMaker Pipeline
   * Creates IAM roles, S3 buckets (optionally)
   * Registers the pipeline using `sagemaker.pipeline.Pipeline`

2. **Pipeline Components (SDK)**:

   * **ProcessingStep**: Cleans and transforms raw data
   * **TrainingStep**: Trains the model using `SKLearn` estimator
   * **ModelStep**: Registers the model with associated metrics
   * **Deploy script**: Uses `boto3` to deploy model as endpoint

---

## 🚀 How to Deploy

Follow these steps to get your SageMaker MLOps pipeline running from scratch.

---

### 🧩 Requirements

Make sure you have the following tools installed:

#### ✅ AWS CLI

```bash
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi
aws --version
```

* Create an IAM User with **programmatic access** and configure your AWS credentials using:

```bash
aws configure
```

#### ✅ Node.js & AWS CDK

```bash
node -v
npm -v
npm install -g aws-cdk
cdk --version
```

#### ✅ Python & Virtual Environment

```bash
python3 --version
pip3 --version
pip install virtualenv
```

---

### 🏗️ Project Setup

Initialize the CDK app (if starting fresh):

```bash
cdk init app --language python
```

Activate the virtual environment:

```bash
.venv\Scripts\activate  # For Windows
# Or use: source .venv/bin/activate  # For Unix/macOS
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

### 📦 Deploy Infrastructure

Replace placeholders with your actual AWS account and region:

```bash
cdk bootstrap aws://<your-account-id>/<region>
cdk deploy
```

---

### 🌀 Run the SageMaker Pipeline

After deploying the infrastructure, trigger the pipeline execution:

```bash
python pipeline/pipeline_definition.py     # Define and register the pipeline
python pipeline/run_pipeline.py            # Trigger pipeline execution
```

---

### 🚀 Deploy and Invoke the Endpoint

Once the pipeline finishes, deploy the model to a live endpoint:

```bash
python deployment/deploy_endpoint.py       # Deletes old endpoint and creates new one
python deployment/invoke_endpoint.py       # Send test request to endpoint
```

---

## 📈 Metrics Example

During training, metrics like the following are generated and automatically stored in S3:

```json
{
  "regression_metrics": {
    "accuracy": {
      "value": 0.755,
      "standard_deviation": 0.0
    }
  }
}
```

These are passed to `ModelMetrics()` to support model governance and CI/CD decision-making.

---

## 💰 Free Tier Considerations

This project is **compatible with AWS Free Tier**, but some parts may incur costs depending on the instance types used:

### ✅ Free Tier-Compatible Components

* **SageMaker endpoints** can use `ml.t2.medium` or `ml.t3.medium`, which are eligible under the Free Tier (up to 250 hours per month for 2 months).
* **Lightweight models and test data** can stay within free-tier storage limits (e.g. S3 and ECR).
* **CDK deployments**, AWS CLI actions, and most SDK-based scripts incur no charges beyond AWS resource usage.

### ⚠️ Components That May Exceed Free Tier

* **Training and Processing jobs** using instance types like `ml.m5.large` or `ml.m5.xlarge` **are not covered** by the Free Tier.
* **Long-running endpoints** or large model artifacts in S3 may accumulate storage or compute costs over time.

### 🔍 Cost-Saving Tips

* When testing, use the smallest acceptable instance types (`ml.t3.medium`, `ml.t2.medium`, `ml.m4.xlarge`, etc.).
* Always shut down endpoints when they’re not needed:

  ```bash
  aws sagemaker delete-endpoint --endpoint-name <your-endpoint-name>
  ```
* Monitor usage in the [AWS Billing Dashboard](https://console.aws.amazon.com/billing/home#/).
* Automate cleanup using `cdk destroy` or lifecycle policies for S3.

---

## 📬 Contact

Created by **\[Johan Zuluaga]**.
For questions, feel free to reach out via \[johandzuluaga@gmail.com].

---

