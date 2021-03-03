from django.db import models

class Drive(models.Model):
    caption = models.CharField(max_length=255)
    compressed = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    provider_name = models.CharField(max_length=255)
    size = models.BigIntegerField()
    system_name = models.CharField(max_length=255)
    volume_name = models.CharField(max_length=255)


def get_drives():
    return Drive.objects.all()
