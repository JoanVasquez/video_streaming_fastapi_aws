# 🗄️ Database imports
from db.db import get_db
from db.models.user import User
from db.models.video import Video
from db.models.video import ProcessingStatus, VisibilityStatus
from sqlalchemy import or_
from fastapi import HTTPException
from pydantic_models.upload_models import UploadMetadata
from pydantic_models.VideoResponse import VideoResponse


class VideoRepository:
    def upload_video_metadata(
        self, metadata: UploadMetadata, user: User
    ) -> VideoResponse:
        try:
            with get_db() as db:
                video = Video(
                    title=metadata.title,
                    description=metadata.description,
                    user_id=user["sub"],
                    video_s3_key=metadata.video_s3_key,
                    visibility=metadata.visibility,
                )
                db.add(video)
                db.commit()
                db.refresh(video)

                # ✅ Este es el modelo de salida correcto
                return VideoResponse.model_validate(video)

        except Exception as e:
            print("❌ Error in upload_video_metadata:", e)
            raise HTTPException(
                status_code=500,
                detail="Failed to upload video metadata."
            )

    def get_all_videos(self) -> list[VideoResponse]:
        try:
            with get_db() as db:
                all_videos = db.query(Video).filter(
                    Video.is_processing == ProcessingStatus.COMPLETED,
                    Video.visibility == VisibilityStatus.PUBLIC,
                ).all()
                return [
                    VideoResponse.model_validate(video) for video in all_videos
                ]
        except Exception as e:
            print("❌ Error in get_all_videos:", e)
            raise HTTPException(
                status_code=500,
                detail="Failed to retrieve videos."
            )

    def get_video_by_id(self, video_id: int) -> VideoResponse:
        try:
            print("video_id", video_id)
            with get_db() as db:
                video = (
                    db.query(Video).filter(
                        Video.id == video_id,
                        Video.is_processing == ProcessingStatus.COMPLETED,
                        or_(
                            Video.visibility == VisibilityStatus.PUBLIC,
                            Video.visibility == VisibilityStatus.UNLISTED
                        ),
                    ).first()
                )

                if not video:
                    raise HTTPException(
                        status_code=404,
                        detail="Video not found or not available."
                    )

                return VideoResponse.model_validate(video)
        except HTTPException as e:
            raise e
        except Exception as e:
            print("❌ Error in get_video_by_id:", e)
            raise HTTPException(
                status_code=500,
                detail="Failed to retrieve video."
            )

    def update_video_by_id(
            self, video_id: int,
    ):
        try:
            with get_db() as db:
                video = db.query(Video).filter(Video.id == video_id).first()
                if not video:
                    raise HTTPException(
                        status_code=404,
                        detail="Video not found."
                    )
                video.is_processing = ProcessingStatus.COMPLETED
                db.commit()
                db.refresh(video)
                return VideoResponse.model_validate(video)
        except HTTPException as e:
            raise e
        except Exception as e:
            print("❌ Error in update_video_by_id:", e)
            raise HTTPException(
                status_code=500,
                detail="Failed to update video."
            )
