from secret_keys import SecretKeys
from db.models.user import User
from repositories.VideoRepository import VideoRepository
from pydantic_models.upload_models import UploadMetadata
import boto3
import uuid


class UploadService:
    def __init__(self):
        secret_keys = SecretKeys()
        REGION_NAME = secret_keys.REGION_NAME
        self.video_repository = VideoRepository()
        self.AWS_RAW_VIDEO_BUCKER = secret_keys.AWS_RAW_VIDEO_BUCKER
        self.AWS_VIDEO_THUMBNAIL_BUCKET = \
            secret_keys.AWS_VIDEO_THUMBNAIL_BUCKET
        self.s3_client = boto3.client('s3', region_name=REGION_NAME)

    def presigned_url(self, user: User):
        try:
            video_id = f"videos/{user['sub']}/{uuid.uuid4()}.mp4"
            response = self.s3_client.generate_presigned_url(
                "put_object",
                Params={
                    "Bucket": self.AWS_RAW_VIDEO_BUCKER,
                    "Key": video_id,
                    "ContentType": "video/mp4",
                },
            )

            return {
                "url": response,
                "video_id": video_id
            }
        except Exception as e:
            print(e)
            return None

    def presigned_url_thumbnail(self, user: User):
        try:
            thumbnail_id = f"{user['sub']}/{uuid.uuid4()}"
            response = self.s3_client.generate_presigned_url(
                "put_object",
                Params={
                    "Bucket": self.AWS_VIDEO_THUMBNAIL_BUCKET,
                    "Key": thumbnail_id,
                    "ContentType": "image/jpg",
                },
            )

            return {
                "url": response,
                "thumbnail_id": thumbnail_id
            }
        except Exception as e:
            print(e)
            return None

    def upload_metadata(
        self, metadata: UploadMetadata, user: User
    ):
        new_video = self.video_repository.upload_video_metadata(
            metadata=metadata,
            user=user
        )

        print(new_video)
        return new_video
