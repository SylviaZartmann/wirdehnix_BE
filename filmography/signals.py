import os
import django_rq
from django.dispatch import receiver
from filmography.models import Filmography
from django.db.models.signals import post_save, post_delete

from filmography.tasks import convert_video


@receiver(post_save, sender=Filmography)
def video_post_save(sender, instance, created, **kwargs):
    # Print messages indicating that a video was saved and if it's a new video
    # Get the default RQ queue with autocommit enabled
    # Define resolutions to convert the video to
    # Enqueue background jobs to convert the video to different resolutions
    
    print("Video was saved")
    if created:
        print("New video was created")                              
        queue = django_rq.get_queue("default", autocommit=True)     
        resolutions = ["480p", "720p", "1080p"]                     
        for resolution in resolutions:                              
            queue.enqueue(convert_video, instance.video_file.path, resolution)


# DONT TOUCH !
@receiver(post_delete, sender=Filmography)
def video_post_delete(sender, instance, **kwargs):
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
    if instance.video_file_480p:
        if os.path.isfile(instance.video_file_480.path):
            os.remove(instance.video_file_480.path)
    if instance.video_file_720p:
        if os.path.isfile(instance.video_file_720p.path):
            os.remove(instance.video_file_720p.path)
    if instance.video_file_1080p:
        if os.path.isfile(instance.video_file_1080p.path):
            os.remove(instance.video_file_1080p.path)
