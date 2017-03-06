from django.db import models
import requests


class Project(models.Model):
    title = models.CharField("Project Title", max_length=500)
    
    def __str__(self):
        tag_count = 0
        for video in self.video_set.all():
            tag_count += video.tag_set.count()
        return "{} [{} Videos, {} Tags]".format(
                self.title,
                self.video_set.count(),
                tag_count)

class Video(models.Model):
    title = models.CharField("Title", max_length=500)
    uploaded_video = models.FileField("Video File", upload_to="videos/")
    project = models.ForeignKey(Project)
    
    def __str__(self):
        return "{} [{} Tags]".format(self.title, self.tag_set.count())

class Tag(models.Model):
    """
        Django model that stores tags of type
            * Text
            * HTML(Remote)
            * Images
            * Video/Audio
            * PHP Survey
            * Maps
    """

    video = models.ForeignKey(Video)
    x = models.IntegerField("X Position")
    y = models.IntegerField("Y Position")
    width = models.IntegerField("Tag Width")
    height = models.IntegerField("Tag Height")
    time_start = models.IntegerField("Time Start")
    time_end = models.IntegerField("Time End")
    remote = models.BooleanField("Remote?")
    local_content = models.TextField("Local Content", blank=True)
    remote_url = models.CharField(max_length=1000, blank=True)
    
    @property
    def resource(self):
        if self.remote:
            response = requests.get(self.remote_url)
            return (response.text(),
                    response.headers["content-type"])
        else:
            return (local_content, 'text/plain')

    def __str__(self):
        return "{} @ ({}, {})[{}-{}]".format(
                self.remote_url if self.remote
                else self.local_content[:47]+"...",
                self.x, 
                self.y, 
                self.time_start, 
                self.time_end)
