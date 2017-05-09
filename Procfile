web: gunicorn config.wsgi:application
worker: celery worker --app=gc_classifier.taskapp --loglevel=info
