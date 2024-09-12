from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='videos/')
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

class Subtitle(models.Model):
    video = models.ForeignKey(Video, related_name='subtitles', on_delete=models.CASCADE)
    language = models.CharField(max_length=50, default='English')
    content = models.TextField()
    timestamp = models.CharField(max_length=50)  

    def __str__(self):
        return f"{self.video} - {self.timestamp}"
