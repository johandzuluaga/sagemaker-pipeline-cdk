import time
import boto3

sagemaker_client = boto3.client("sagemaker", region_name="us-east-1")

# 1. Get the latest approved model package
response = sagemaker_client.list_model_packages(
    ModelPackageGroupName="TitanicModelPackageGroup",
    ModelApprovalStatus="Approved",
    SortBy="CreationTime",
    SortOrder="Descending",
    MaxResults=1
)

model_package_arn = response["ModelPackageSummaryList"][0]["ModelPackageArn"]

# 2. Create a model from the package
model_name = "titanic-model-deployment"

try:
    sagemaker_client.delete_model(ModelName=model_name)
    print(f"Deleted existing model: {model_name}")
except sagemaker_client.exceptions.ClientError as e:
    if "Could not find model" not in str(e):
        raise

create_model_response = sagemaker_client.create_model(
    ModelName=model_name,
    ExecutionRoleArn="arn:aws:iam::728611193981:role/SageMakerTestStack-SageMakerExecutionRole7843F3B8-ue6AtEtiCRPx",
    PrimaryContainer={
        "ModelPackageName": model_package_arn
    }
)

# 3. Create an endpoint configuration
endpoint_config_name = "titanic-endpoint-config"

try:
    sagemaker_client.delete_endpoint_config(EndpointConfigName=endpoint_config_name)
    print(f"Deleted previous endpoint config: {endpoint_config_name}")
except sagemaker_client.exceptions.ClientError as e:
    if "Could not find endpoint configuration" not in str(e):
        raise

create_endpoint_config_response = sagemaker_client.create_endpoint_config(
    EndpointConfigName=endpoint_config_name,
    ProductionVariants=[
        {
            "VariantName": "AllTraffic",
            "ModelName": model_name,
            "InitialInstanceCount": 1,
            "InstanceType": "ml.t2.medium",
            "InitialVariantWeight": 1
        }
    ]
)

# 4. Deploy the endpoint
endpoint_name = "titanic-endpoint"

try:
    sagemaker_client.delete_endpoint(EndpointName=endpoint_name)
    print(f"Deleted previous endpoint: {endpoint_name}")

    # Wait for deletion to complete
    while True:
        try:
            response = sagemaker_client.describe_endpoint(EndpointName=endpoint_name)
            status = response["EndpointStatus"]
            print(f"Waiting for endpoint deletion... Current status: {status}")
            time.sleep(10)
        except sagemaker_client.exceptions.ClientError as e:
            if "Could not find endpoint" in str(e):
                print(f"Endpoint {endpoint_name} deleted.")
                break
            else:
                raise

except sagemaker_client.exceptions.ClientError as e:
    if "Could not find endpoint" not in str(e):
        raise

create_endpoint_response = sagemaker_client.create_endpoint(
    EndpointName=endpoint_name,
    EndpointConfigName=endpoint_config_name
)

print(f"Endpoint '{endpoint_name}' is being created.")
