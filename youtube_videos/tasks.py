# tasks.py

from celery import shared_task
import aiohttp
import asyncio
from .models import Video
from decouple import config

from asgiref.sync import async_to_sync, sync_to_async

@sync_to_async
def get_or_create_video(video_id, item):
    video, created = Video.objects.get_or_create(id=video_id)
    video.title = item['snippet']['title']
    video.description = item['snippet']['description']
    video.published_at = item['snippet']['publishedAt']
    video.thumbnail_url = item['snippet']['thumbnails']['high']['url']
    video_url = f"https://www.youtube.com/watch?v={item['id']['videoId']}"
    video.video_url = video_url  

    video.save()


async def fetch_videos():
    api_url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'part': 'snippet',
        'q': 'search',  # Example search query
        'order': 'date',
        'type': 'video',
        'key': 'AIzaSyBCoB7-XLvG4d2v4eZYEw2Blh3tKcgnGy8'
    }

    async with aiohttp.ClientSession() as session:
        response = await session.get(api_url, params=params)
        data = await response.json()
        print("data::", data)
        for item in data['items']:
            video_id = item['id']['videoId']
            await get_or_create_video(video_id, item)


@shared_task(name="youtube_videos.tasks.fetch_videos_task")
def fetch_videos_task():
    asyncio.run(fetch_videos())
