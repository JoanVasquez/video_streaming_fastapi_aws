# 🎥 Video Transcoding Service
# Handles downloading, transcoding and uploading of video files to S3
import os
from pathlib import Path
import boto3
import requests
import mimetypes
from secret_keys import SecretKeys
from transcode_video import transcode_video


class VideoTranscoder:
    def __init__(self):
        self.secret_keys = SecretKeys()  # ✅ CORRECTO

        self.s3_client = boto3.client(
            "s3",
            region_name=self.secret_keys.REGION_NAME,
            aws_access_key_id=self.secret_keys.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self.secret_keys.AWS_SECRET_ACCESS_KEY
        )

    def _get_content_type(self, file_path: str):
        # 📁 Determine content type based on file extension
        mime_type, _ = mimetypes.guess_type(file_path)
        return mime_type or "application/octet-stream"

    def download_video(self, local_path):
        # ⬇️ Download video from S3 bucket
        self.s3_client.download_file(
            self.secret_keys.S3_BUCKET,
            self.secret_keys.S3_KEY,
            local_path
        )

    def upload_files(self, prefix: str, local_dir):
        # ⬆️ Upload processed files to S3
        for root, _, files in os.walk(local_dir):
            for file in files:
                local_path = os.path.join(root, file)
                s3_key = f"{prefix}/{os.path.relpath(local_path, local_dir)}"
                self.s3_client.upload_file(
                    local_path,
                    self.secret_keys.S3_PROCESSED_VIDEOS_BUCKET,
                    s3_key,
                    ExtraArgs={
                        "ACL": "public-read",
                        "ContentType": self._get_content_type(local_path),
                    },
                )

    def process_video(self):
        # 🎬 Main video processing workflow
        work_dir = Path("/tmp/workspace")
        work_dir.mkdir(exist_ok=True)
        input_path = work_dir / "input.mp4"
        output_path = work_dir / "output"
        output_path.mkdir(exist_ok=True)

        try:
            # 1️⃣ Download video
            self.download_video(input_path)
            # 2️⃣ Transcode video
            transcode_video(str(input_path), str(output_path))
            # 3️⃣ Upload processed files
            self.upload_files(self.secret_keys.S3_KEY, str(output_path))
            self.update_video()
        finally:
            # 🧹 Cleanup temporary files
            if input_path.exists():
                input_path.unlink()
            if output_path.exists():
                import shutil
                shutil.rmtree(output_path)

    def update_video(self):
        # 🔄 Update video status in backend
        try:
            response = requests.put(
                f"{self.secret_keys.BACKEND_URL}/videos"
                f"?id={self.secret_keys.S3_KEY}"
            )
            print(response.json())
            return response.json()
        except Exception as e:
            print(e)


# 🚀 Start video processing
VideoTranscoder().process_video()
