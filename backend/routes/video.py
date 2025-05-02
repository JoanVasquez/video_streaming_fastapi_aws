from fastapi import APIRouter, Depends, HTTPException
from db.middleware.auth_middleware import get_current_user
from services.VideoService import VideoService
from pydantic_models.VideoResponse import VideoResponse

router = APIRouter()


@router.get("/all")
def get_all_videos(
    user=Depends(get_current_user),
    upload_service: VideoService = Depends(VideoService),
):
    try:
        return upload_service.get_all_videos()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{video_id}", response_model=VideoResponse)
def get_video_by_id(
    video_id: str,
    user=Depends(get_current_user),
    upload_service: VideoService = Depends(VideoService),
):
    try:
        return upload_service.get_video_by_id(video_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{video_id}")
def update_video(
    video_id: str,
    upload_service: VideoService = Depends(VideoService),
):
    try:
        return upload_service.update_video_by_id(video_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
