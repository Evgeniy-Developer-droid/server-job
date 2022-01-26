from django.db import models


class Job(models.Model):
    ip = models.CharField(max_length=255)
    useragent = models.CharField(max_length=500)
    url = models.CharField(max_length=500)
    token = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    result = models.TextField(default="{}")

    def save(self, *args, **kwargs):
        super(Job, self).save(*args, **kwargs)
        return self


class SlaveServer(models.Model):
    url = models.URLField()

    def __str__(self):
        return self.url
