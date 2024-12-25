from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from youtube_videos.models import Video
from rest_framework.pagination import PageNumberPagination
import asyncio
from youtube_videos.tasks import fetch_videos
from .serializers import *

class VideoFetchView(APIView):
    def get(self, request):

        asyncio.create_task(fetch_videos())
        return Response({"message": "Video fetching started"}, status=status.HTTP_200_OK)

class VideoPagination(PageNumberPagination):
    page_size = 10  # Limited to 10 results per page, we can  change according to our need

class VideoListView(APIView):
    def get(self, request):
      
        search_query = request.GET.get('search', None)

        if search_query:
            videos = Video.objects.filter(title__icontains=search_query).order_by('-published_at')
            print("videos:",videos)
        else:
            videos = Video.objects.all().order_by('-published_at')

        paginator = VideoPagination()
        paginated_videos = paginator.paginate_queryset(videos, request)

        serializer = VideoSerializer(paginated_videos, many=True)

        return paginator.get_paginated_response(serializer.data)
