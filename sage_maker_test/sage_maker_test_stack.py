from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    RemovalPolicy,
)
from constructs import Construct
from pathlib import Path

class SageMakerTestStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Raw data bucket
        raw_data_bucket = s3.Bucket(self, "RawDataBucket",
            bucket_name="ml-raw-data-johan",
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        # Processed data bucket
        processed_data_bucket = s3.Bucket(self, "ProcessedDataBucket",
            bucket_name="ml-processed-data-johan",
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        # Deploy Titanic CSV to raw bucket
        s3deploy.BucketDeployment(self, "UploadTitanicDataset",
            destination_bucket=raw_data_bucket,
            sources=[s3deploy.Source.asset(str(Path(__file__).parent.parent / "data"))],
            destination_key_prefix="titanic",
        )
