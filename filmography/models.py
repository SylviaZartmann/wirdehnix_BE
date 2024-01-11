import datetime
from django.db import models

CATEGORY_CHOICE = [
    ('F', 'Fiction'),
    ('D', 'Documentary'),
    ('A', 'Animation'),
    ('H', 'Horror')
]
class Filmography(models.Model):
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    category = models.CharField(default='', choices=CATEGORY_CHOICE, max_length=50)
    video_file = models.FileField(upload_to='videos', blank=True, null=True)
    video_file_480p = models.FileField(upload_to='videos', blank=True, null=True)
    video_file_720p = models.FileField(upload_to='videos', blank=True, null=True)
    video_file_1080p = models.FileField(upload_to='videos', blank=True, null=True)
    thumbnail = models.FileField(upload_to='thumbnails', blank=True, null=True)
    upload_date = models.DateField(default=datetime.date.today)