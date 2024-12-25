from django.db import models

class Video(models.Model):
    id = models.CharField(max_length=255, primary_key=True) 
    title = models.CharField(max_length=255)
    description = models.TextField()
    published_at = models.DateTimeField(null=True, blank=True) 

    thumbnail_url = models.URLField(null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title
