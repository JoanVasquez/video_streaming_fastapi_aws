from fastapi import APIRouter, Depends, HTTPException
from db.middleware.auth_middleware import get_current_user
from services.UploadService import UploadService
from pydantic_models.upload_models import UploadMetadata
from pydantic_models.VideoResponse import VideoResponse

router = APIRouter()


@router.get("/url")
def get_presigned_url(
    user=Depends(get_current_user),
    upload_service: UploadService = Depends(UploadService)
):
    try:
        return upload_service.presigned_url(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/url/thumbnail")
def get_presigned_url_thumbnail(
    user=Depends(get_current_user),
    upload_service: UploadService = Depends(UploadService)
):
    try:
        return upload_service.presigned_url_thumbnail(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/metadata", response_model=VideoResponse)
def upload_metadata(
    metadata: UploadMetadata,
    user=Depends(get_current_user),
    upload_service: UploadService = Depends(UploadService)
):
    try:
        return upload_service.upload_metadata(metadata, user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
