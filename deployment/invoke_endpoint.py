import boto3

runtime = boto3.client("sagemaker-runtime")

response = runtime.invoke_endpoint(
    EndpointName="titanic-endpoint",
    ContentType="text/csv",  # or "application/json", depending on your model
    # Pclass, Sex, Age, SibSp, Parch, Fare, Embarked
    Body="3,1,22.0,1,0,7.25,0"
)

result = response["Body"].read().decode("utf-8")
print("Prediction:", result)
