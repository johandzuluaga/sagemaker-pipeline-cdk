from pathlib import Path
import sagemaker
from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.workflow.steps import ProcessingStep
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.processing import ProcessingInput, ProcessingOutput
from sagemaker.sklearn.estimator import SKLearn
from sagemaker.workflow.steps import TrainingStep
from sagemaker.inputs import TrainingInput
import os

sagemaker_session = sagemaker.session.Session()
role_arn = "arn:aws:iam::728611193981:role/SageMakerTestStack-SageMakerExecutionRole7843F3B8-ue6AtEtiCRPx"
bucket_raw = "ml-raw-data-johan"
bucket_processed = "ml-processed-data-johan"

script_processor = SKLearnProcessor(
    framework_version="0.23-1",
    role=role_arn,
    instance_type="ml.t3.medium",
    instance_count=1,
    base_job_name="titanic-preprocessing",
    sagemaker_session=sagemaker_session
)

processing_step = ProcessingStep(
    name="TitanicPreprocessingStep",
    processor=script_processor,
    inputs=[
        ProcessingInput(
            source=f"s3://{bucket_raw}/titanic/titanic.csv",
            destination="/opt/ml/processing/input"
        )
    ],
    outputs=[
        ProcessingOutput(
            output_name="train_data",
            source="/opt/ml/processing/output/train",
            destination=f"s3://{bucket_processed}/titanic/train"
        )
    ],
    code="scripts/preprocessing.py"
)

# Define SKLearn Estimator
sklearn_estimator = SKLearn(
    entry_point="scripts/train.py",
    role=role_arn,
    instance_type="ml.m5.large",
    framework_version="0.23-1",
    instance_count=1,
    base_job_name="titanic-train",
    sagemaker_session=sagemaker_session,
)

# Define TrainingStep
training_step = TrainingStep(
    name="TrainModel",
    estimator=sklearn_estimator,
    inputs={
        "train": TrainingInput(
            s3_data=processing_step.properties.ProcessingOutputConfig.Outputs["train_data"].S3Output.S3Uri,
            content_type="text/csv",
        )
    },
)

pipeline = Pipeline(
    name="TitanicPipeline",
    steps=[processing_step, training_step],
    sagemaker_session=sagemaker_session
)

pipeline.upsert(role_arn=role_arn)
