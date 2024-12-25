from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from youtube_videos.models import Video
from rest_framework.pagination import PageNumberPagination
import asyncio
from youtube_videos.tasks import fetch_videos

class VideoFetchView(APIView):
    def get(self, request, *args, **kwargs):

        asyncio.create_task(fetch_videos())
        return Response({"message": "Video fetching started"}, status=status.HTTP_200_OK)

class VideoPagination(PageNumberPagination):
    page_size = 10  # Limited to 10 results per page, we can  change according to our need

class VideoListView(APIView):
    def get(self, request):
        videos = Video.objects.all().order_by('-published_at')

       
        paginator = VideoPagination()
        paginated_videos = paginator.paginate_queryset(videos, request)

        video_data = [
            {
                "title": video.title,
                "description": video.description,
                "published_at": video.published_at,
                "thumbnail_url": video.thumbnail_url,
                "video_url": video.video_url
            }
            for video in paginated_videos
        ]

        return paginator.get_paginated_response(video_data)


