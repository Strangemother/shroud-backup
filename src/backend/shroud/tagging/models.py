from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=255)
    bulk_id = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name


class Entry(models.Model):
    filepath = models.CharField(max_length=2055)
    tags = models.ManyToManyField(Tag)#, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.filepath} Tags: {self.tags.count()}"
