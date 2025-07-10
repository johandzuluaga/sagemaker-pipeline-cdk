from sagemaker.workflow.pipeline import Pipeline
from sagemaker.session import Session

sagemaker_session = Session()

role = "arn:aws:iam::728611193981:role/SageMakerTestStack-SageMakerExecutionRole7843F3B8-ue6AtEtiCRPx"

pipeline_name = "TitanicPipeline"

pipeline = Pipeline(
    name=pipeline_name,
    sagemaker_session=sagemaker_session
)

execution = pipeline.start()

print(f"Pipeline execution started: {execution.arn}")
