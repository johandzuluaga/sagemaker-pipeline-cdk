import sagemaker
# Data preprocessing imports
from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.workflow.steps import ProcessingStep
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.processing import ProcessingInput, ProcessingOutput
# Model training imports
from sagemaker.sklearn.estimator import SKLearn
from sagemaker.workflow.steps import TrainingStep
from sagemaker.inputs import TrainingInput
# Model registration imports
from sagemaker.workflow.model_step import ModelStep
from sagemaker.model_metrics import MetricsSource, ModelMetrics
from sagemaker.workflow.model_step import ModelStep
from sagemaker.sklearn.model import SKLearnModel
from sagemaker.workflow.pipeline_context import PipelineSession

from sagemaker.workflow.functions import Join

pipeline_session = PipelineSession()

role_arn = "arn:aws:iam::728611193981:role/SageMakerTestStack-SageMakerExecutionRole7843F3B8-ue6AtEtiCRPx"
bucket_raw = "ml-raw-data-johan"
bucket_processed = "ml-processed-data-johan"

script_processor = SKLearnProcessor(
    framework_version="0.23-1",
    role=role_arn,
    instance_type="ml.t3.medium",
    instance_count=1,
    base_job_name="titanic-preprocessing",
    sagemaker_session=pipeline_session
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
    entry_point="train.py",
    source_dir="scripts",
    role=role_arn,
    instance_type="ml.m5.large",
    framework_version="0.23-1",
    instance_count=1,
    base_job_name="titanic-train",
    sagemaker_session=pipeline_session,
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

metrics_s3_uri = Join(
    on="/",
    values=[
        training_step.properties.ModelArtifacts.S3ModelArtifacts,
        "..",  # go up from model.tar.gz
        "metrics/metrics.json"
    ]
)

# Create model metrics object
model_metrics = ModelMetrics(
    model_statistics=MetricsSource(
        s3_uri=metrics_s3_uri,
        content_type="application/json"
    )
)

# Define the model using pipeline runtime output
model = SKLearnModel(
    model_data=training_step.properties.ModelArtifacts.S3ModelArtifacts,
    entry_point='inference.py',
    source_dir='scripts',
    image_uri=sklearn_estimator.training_image_uri(),
    role=role_arn,
    sagemaker_session=pipeline_session
)

# Register the model (deferred via step_args)
register_model_step = ModelStep(
    name="RegisterTitanicModel",
    step_args=model.register(
        content_types=["text/csv"],
        response_types=["text/csv"],
        inference_instances=["ml.t2.medium"],
        transform_instances=["ml.m5.large"],
        model_package_group_name="TitanicModelPackageGroup",
        approval_status="Approved",
        description="Titanic survival prediction model",
        model_metrics=model_metrics
    )
)

pipeline = Pipeline(
    name="TitanicPipeline",
    steps=[
        processing_step,
        training_step,
        register_model_step
    ],
    sagemaker_session=pipeline_session
)

pipeline.upsert(role_arn=role_arn)
