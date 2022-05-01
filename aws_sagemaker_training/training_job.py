import argparse
import os

import boto3
import sagemaker
from sagemaker.session import TrainingInput
from sagemaker.estimator import Estimator


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--role_arn", type=str)
    parser.add_argument("--input_s3", type=str, default="test-sagemaker-input-data")
    parser.add_argument("--input_file", type=str, default="input.txt")
    parser.add_argument("--use_gpu", action="store_true")
    args = parser.parse_args()

    sess = sagemaker.Session()

    account_id = boto3.client("sts").get_caller_identity().get("Account")
    ecr_image = os.getenv("ECR_IMAGE", "tf-custom-container")
    tag = ":latest"

    region = boto3.session.Session().region_name

    uri_suffix = "amazonaws.com"
    if region in ["cn-north-1", "cn-northwest-1"]:
        uri_suffix = "amazonaws.com.cn"

    byoc_image_uri = "{}.dkr.ecr.{}.{}/{}".format(
        account_id, region, uri_suffix, ecr_image + tag)

    train_input = TrainingInput(
        "s3://{}/{}".format(args.input_s3, args.input_file), content_type="txt"
    )

    parameters = {
        "image_uri": byoc_image_uri,
        "role": args.role_arn,
        "instance_count": 1,
        "environment": {"TESTING_ENV": "FOUND"},
        "instance_type": "ml.m5.xlarge"  # Free tier CPU instance
    }

    if args.use_gpu:
        print("Using a GPU instance")
        parameters["instance_type"] = "ml.g4dn.xlarge"  # T4 GPU instance

    estimator = Estimator(**parameters)

    estimator.fit({"training": train_input})
