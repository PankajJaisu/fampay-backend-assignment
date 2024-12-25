# tasks.py
from itertools import cycle


from celery import shared_task
import aiohttp
import asyncio
from .models import Video
from decouple import config
import random
from asgiref.sync import sync_to_async

# Fetching API keys from environment variables
api_keys = config('YOUTUBE_API_KEY').split(',')
api_key_cycle = cycle(api_keys)

def get_next_api_key():
    return next(api_key_cycle)


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
    # Getting search query from environment variable
    search_query = config('YOUTUBE_SEARCH_QUERY', default='cricket')  # Using 'cricket' if not defined

    api_url = 'https://www.googleapis.com/youtube/v3/search'

    api_key = get_next_api_key()

    if not api_key:
        print("All API keys exhausted. Stopping task.")
        return

    while True:
        params = {
            'part': 'snippet',
            'q': search_query,
            'order': 'date',
            'type': 'video',
            'key': api_key
        }

        async with aiohttp.ClientSession() as session:
            response = await session.get(api_url, params=params)

            if response.status == 200:
                data = await response.json()
                for item in data['items']:
                    video_id = item['id']['videoId']
                    await get_or_create_video(video_id, item)
                break

            elif response.status == 403:
                print(f"API key {api_key} exhausted, trying the next one.")
                api_key = get_next_api_key()
                if not api_key:
                    print("All API keys exhausted. Stopping task.")
                    break
                continue

            else:
                print(f"Error occurred: {response.status}")
                break


@shared_task(name="youtube_videos.tasks.fetch_videos_task")
def fetch_videos_task():
    asyncio.run(fetch_videos())
