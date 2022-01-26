from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Job
import uuid


@receiver(post_save, sender=Job)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.token = str(uuid.uuid4())
        instance.save()
