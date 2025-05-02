import json
from db.redis_db import redis_client
from repositories.VideoRepository import VideoRepository
from pydantic_models.VideoResponse import VideoResponse


class VideoService:
    def __init__(self):
        self.video_repository = VideoRepository()

    def get_all_videos(self) -> list:
        return self.video_repository.get_all_videos()

    def get_video_by_id(self, video_id: int):
        cache_key = f"video:{video_id}"
        cached_video = redis_client.get(cache_key)
        if cached_video:
            return VideoResponse.model_validate(json.loads(cached_video))

        video = self.video_repository.get_video_by_id(video_id)
        if video:
            redis_client.setex(cache_key, 3600, video.model_dump_json())

        return video

    def update_video_by_id(self, video_id: int):
        cache_key = f"video:{video_id}"
        cached_video = redis_client.get(cache_key)
        if cached_video:
            redis_client.delete(cache_key)

        return self.video_repository.update_video_by_id(video_id)
