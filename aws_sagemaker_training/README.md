# AWS Configuration steps

- [Install AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

- From IAM service create a new user and grant needed permissions or attach an existing policy (like AdministratorAccess) to the user.

- [Configure AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html) with the Access Key ID and Secret Access Key obtained in the previous step.

- From IAM service create a new Role with Sagemaker permissions and save the resulting ARN string (follows a structure like this arn:aws:iam::111111111111:role/rolename), it will be pass as an argument to the job trigger.

- (Optional) Request access to GPUs. It can be done by creating a new case requesting a limit increase from the [AWS Support Center](https://us-east-1.console.aws.amazon.com/support/home). Note it can take up to a few weeks. 

*[AWS Sagemaker Training Free Tier](https://aws.amazon.com/sagemaker/pricing) includes 50 hours of m4.xlarge or m5.xlarge instances*

# Serverless job configuration

- Create a S3 bucket and upload training data

- Create an enviroment and install requirements:

```
python3 -m venv env
source env/bin/activate
pip3 install -U pip
pip3 install -r requirements.txt
```

- Customize `train.py` file your training code.

- Set Docker image name:

```
export ECR_IMAGE=tf-custom-container
```

- Build and push the image to ECR:

```
bash push_docker_image.sh
```

- Trigger job:

```
python training_job.py --role_arn <your-role> --input_s3 <your-s3-bucket> --input_file <path-to-your-file>
```

*NOTE: Bucket input data will be available in `/opt/ml/input/data/training`. Output model can be saved in `/opt/ml/model/`*
