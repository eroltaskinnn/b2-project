import os

from celery import Celery
from celery.schedules import crontab

from dotenv import load_dotenv

from core.config import settings


load_dotenv()


# Create Celery instance
def create_celery_app():
    # Use environment variable or default to redis
    broker_url = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    backend_url = os.getenv('CELERY_BACKEND_URL', 'redis://localhost:6379/0')

    celery_app = Celery(
        'worker',
        broker=broker_url,
        backend=backend_url,
        include=['tasks.library_tasks']
    )

    # Celery configuration
    celery_app.conf.update(
        timezone='UTC',
        enable_utc=True,
        task_track_started=True,
        task_time_limit=30 * 60,  # 30 minutes
        worker_prefetch_multiplier=1,

        # Beat Schedule
        beat_schedule={
            'daily-overdue-reminders': {
                'task': 'tasks.library_tasks.send_overdue_reminders',
                 'schedule': crontab(minute=0, hour=9),  # Run daily at 9 AM
            },
            'weekly-checkout-report': {
                'task': 'tasks.library_tasks.generate_weekly_report',
                'schedule': crontab(day_of_week='monday', hour=0, minute=0),  # Run Monday at midnight
            }
        }
    )

    return celery_app

# Create Celery app instance
celery_app = create_celery_app()