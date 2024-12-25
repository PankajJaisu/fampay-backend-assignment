import asyncio
from googleapiclient.discovery import build
from youtube_videos.models import Video
from datetime import datetime, timedelta
from decouple import config

API_KEYS = config('YOUTUBE_API_KEY').split(',')
current_api_key_index = 0

def get_youtube_api():
    global current_api_key_index
    api_key = API_KEYS[current_api_key_index]
    return build('youtube', 'v3', developerKey=api_key)

async def fetch_videos():
    global current_api_key_index
    search_query = "official"
    next_page_token = None
    youtube = get_youtube_api()

    while True:
        request = youtube.search().list(
            q=search_query,
            type='video',
            order='date',
            pageToken=next_page_token,
            part='snippet'
        )

        try:
            response = request.execute()
        except Exception:
            current_api_key_index = (current_api_key_index + 1) % len(API_KEYS)
            youtube = get_youtube_api()
            continue

        for item in response['items']:
            Video.objects.create(
                title=item['snippet']['title'],
                description=item['snippet']['description'],
                published_at=item['snippet']['publishedAt'],
                thumbnail_url=item['snippet']['thumbnails']['default']['url'],
                video_url=f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            )

        next_page_token = response.get('nextPageToken')
        await asyncio.sleep(10)  # Fetch videos every 10 seconds
