from celery import Celery
from app import create_app

# Celery configuration
celery = Celery(__name__, broker='redis://redis:6379/0', backend='redis://redis:6379/0')

# Replace 'app' with the actual name of your Flask application package
celery.conf.update(
    result_expires=3600,
)

# Optional configuration, see the application user guide.
celery.autodiscover_tasks(['app'])

if __name__ == '__main__':
    celery.start()
