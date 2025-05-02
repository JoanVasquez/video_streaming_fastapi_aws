# pydantic_models/video_response.py
from pydantic import BaseModel
from enum import Enum


class VisibilityStatus(str, Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"
    UNLISTED = "UNLISTED"


class ProcessingStatus(str, Enum):
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    IN_PROGRESS = "IN_PROGRESS"


class VideoResponse(BaseModel):
    id: int
    title: str
    description: str
    user_id: str
    video_s3_key: str
    visibility: VisibilityStatus
    is_processing: ProcessingStatus

    model_config = {
        "from_attributes": True
    }
