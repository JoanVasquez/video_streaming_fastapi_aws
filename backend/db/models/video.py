from db.base import Base
from sqlalchemy import Column, Integer, TEXT, ForeignKey, Enum
import enum


class VisibilityStatus(enum.Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"
    UNLISTED = "UNLISTED"


class ProcessingStatus(enum.Enum):
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    IN_PROGRESS = "IN_PROGRESS"


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True)
    title = Column(TEXT)
    description = Column(TEXT)
    user_id = Column(TEXT, ForeignKey("users.cognito_sub"))
    video_s3_key = Column(TEXT)
    visibility = Column(Enum(
        VisibilityStatus),
        nullable=False,
        default=VisibilityStatus.PRIVATE
    )
    is_processing = Column(Enum(
        ProcessingStatus),
        nullable=False,
        default=ProcessingStatus.IN_PROGRESS
    )

    model_config = {
        "from_attributes": True
    }
