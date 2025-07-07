import boto3

runtime = boto3.client("sagemaker-runtime")

response = runtime.invoke_endpoint(
    EndpointName="titanic-model-deployment",
    ContentType="text/csv",  # or "application/json", depending on your model
    Body="3,1,22.0,1,0,7.25"  # Example Titanic input (adapt to your features!)
)

result = response["Body"].read().decode("utf-8")
print("Prediction:", result)
