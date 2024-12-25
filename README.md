# YouTube Video Fetcher

## Overview

The **YouTube Video Fetcher** is a Django-based application that continuously fetches the latest YouTube videos based on a predefined search query. The application stores essential video details in a database and provides an API to retrieve this data in a paginated, reverse-chronological order.

## Features


- **Continuous Video Fetching:** Periodically fetches the latest YouTube videos for a predefined search query.
- **Database Storage:** Stores video details such as title, description, publishing date-time, and thumbnail URLs.
- **Paginated API:** Provides a paginated API endpoint to retrieve stored videos, sorted in descending order of publishing date-time.
- **API Key Management:** Supports multiple API keys; automatically switches to the next available key if the current one is exhausted.
- **Video Dashboard:** A React-based dashboard to view the stored videos with filtering, sorting, and pagination options.


## Prerequisites

- Python 3.8 or higher
- Django 3.x or higher
- Celery for asynchronous task management
- YouTube Data API v3 keys

## Installation

### 1. **Clone the Repository:**

   ```bash
   git clone https://github.com/PankajJaisu/fampay-backend-assignment.git
   cd fampay-backend-assignment
   ```
### 2. Set Up Virtual Environment for Django Backend
   ```bash
   python3 -m venv venv
   source venv/bin/activate
```

### 3. Install the Requirement
   ```bash
   pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a .env file in the project root and add the following variables:
```bash
YOUTUBE_SEARCH_QUERY=investment
YOUTUBE_API_KEYS='AIzaSyBi-rIY_MUSkORfgGKWROlQOwDt8Su_2HM',
DB_NAME=neondb
DB_USER=neondb_owner
DB_PASSWORD=4yFXHqrQRl8v
DB_HOST=ep-still-bird-a5fodpot.us-east-2.aws.neon.tech
DB_PORT=5432


```

note Added DB credentials directly in .env for assignment purposes to simplify setup and testing. Note: This is not recommended for real-world projects; sensitive data should always be managed securely
## Install Redis 

### 5. Install Redis (for Celery)
On Windows:
- Download and install Redis from [Redis for Windows](https://github.com/microsoftarchive/redis/releases).
- Run Redis as a background service or in a terminal window by executing the Redis executable.


### On macOS:

```
brew install redis
```

### 6.Apply Database Migrations
 
```
python manage.py migrate
```

### 7.Run the Django Server
 
```
python manage.py runserver
```

## Running Celery with Redis

### Start Redis Server

#### On Windows:
Run Redis as a background service or in a terminal window by executing the Redis executable.

#### On macOS:
```bash
redis-server
```

### Start Celery Worker
```bash
celery -A youtube_videos worker --loglevel=info
```

### Start Celery Beat 
Start Celery Beat (for scheduling periodic video fetching every 10 seconds) 
```
celery -A youtube_videos beat --loglevel=info
```

## Demo Link (for Viewing the Dashboard)
To view the React-based dashboard, which displays the stored YouTube videos, visit the following link:

**Demo Link:** [Click here](http://your-demo-link.com)

This dashboard allows you to:

- View stored videos
- Filter by search query
- Sort by published date-time
- Paginate through the videos


### API Request for Fetching YouTube Videos

To retrieve the stored YouTube videos, you can use the following API endpoint:

**Endpoint:**

GET http://127.0.0.1:8000/api/youtube/videos/


**Query Parameters:**

- `search`: The search query to filter the videos (e.g., `cricket`, `football`, etc.).
- `page`: The page number for pagination (e.g., `1`, `2`, etc.).

**Example Request:**

```bash
GET http://127.0.0.1:8000/api/youtube/videos/?search=cricket&page=1
```



