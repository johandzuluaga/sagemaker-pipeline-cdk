from sagemaker.workflow.pipeline import Pipeline
from sagemaker.session import Session

# Your AWS SageMaker session
sagemaker_session = Session()

# Get the default SageMaker role or hardcode your role ARN if needed
role = "arn:aws:iam::728611193981:role/SageMakerTestStack-SageMakerExecutionRole7843F3B8-ue6AtEtiCRPx"

# Pipeline name must match the one you defined in `pipeline_definition.py`
pipeline_name = "TitanicPipeline"  # or the name you set explicitly

# Load the pipeline by name
pipeline = Pipeline(
    name=pipeline_name,
    sagemaker_session=sagemaker_session
)

# Start the execution
execution = pipeline.start()

print(f"Pipeline execution started: {execution.arn}")
