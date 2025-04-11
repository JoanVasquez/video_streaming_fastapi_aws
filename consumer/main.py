# 🔄 Import required libraries
import json
import boto3
from secret_keys import SecretKeys
import urllib.parse

# 🔑 Initialize secret keys and AWS clients
secret_keys = SecretKeys()
sqs_client = boto3.client(
    "sqs",
    region_name=secret_keys.REGION_NAME,
)

ecs_client = boto3.client(
    "ecs",
    region_name=secret_keys.REGION_NAME,
)


# 📥 Poll SQS queue for messages
def poll_sqs():
    while True:
        # 🔍 Receive message from queue
        response = sqs_client.receive_message(
            QueueUrl=secret_keys.AWS_SQS_VIDEO_PROCESSING,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10,
        )

        for message in response.get("Messages", []):
            # 📝 Parse message body
            message_body = json.loads(message.get("Body"))

            # ✅ Check if test event and skip if so
            if (
                "Service" in message_body
                and "Event" in message_body
                and message_body.get("Event") == "s3:TestEvent"
            ):
                sqs_client.delete_message(
                    QueueUrl=secret_keys.AWS_SQS_VIDEO_PROCESSING,
                    ReceiptHandle=message["ReceiptHandle"],
                )
                continue

            # 🎥 Process video transcoding request
            if "Records" in message_body:
                # 📦 Get S3 bucket and key info
                s3_record = message_body["Records"][0]["s3"]
                bucket_name = s3_record["bucket"]["name"]
                s3_key = urllib.parse.unquote_plus(s3_record["object"]["key"])

                # 🚀 Launch ECS Fargate task
                response = ecs_client.run_task(
                    cluster=secret_keys.AWS_ECS_CLUSTER_ARN,
                    launchType="FARGATE",
                    taskDefinition=secret_keys.AWS_ECS_CLUSTER_TASK_ARN,
                    overrides={
                        "containerOverrides": [
                            {
                                "name": "video-transcoder",
                                "environment": [
                                    {
                                        "name": "S3_BUCKET",
                                        "value": bucket_name,
                                    },
                                    {"name": "S3_KEY", "value": s3_key},
                                ],
                            }
                        ]
                    },
                    networkConfiguration={
                        "awsvpcConfiguration": {
                            "subnets": [
                                secret_keys.AWS_VPC_PUBLIC_SUBNET_A,
                                secret_keys.AWS_VPC_PUBLIC_SUBNET_B,
                            ],
                            "assignPublicIp": "ENABLED",
                            "securityGroups": [
                                secret_keys.AWS_VPC_SECURITY_GROUP
                            ],
                        }
                    },
                )

                # 📤 Print response and delete processed message
                print(response)
                sqs_client.delete_message(
                    QueueUrl=secret_keys.AWS_SQS_VIDEO_PROCESSING,
                    ReceiptHandle=message["ReceiptHandle"],
                )


# 🏃 Start polling
poll_sqs()
