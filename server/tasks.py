from celery import shared_task
# from .celery import app
from celery.utils.log import get_task_logger
from datetime import datetime, timedelta

logger = get_task_logger(__name__)


@shared_task
def jobs_cleaner():
    from job_delegate.models import Job
    one_week_ago = datetime.today() - timedelta(7)
    Job.objects.filter(created_at__lt=one_week_ago).delete()

