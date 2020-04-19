from celery import Celery


config = {
    'CELERY_BROKER_URL': 'redis://localhost:6379/0',
    'result_backend': 'redis://localhost:6379/0'
}

celery_app = Celery('api.app', broker=config['CELERY_BROKER_URL'], include=['api.app'])
celery_app.conf.update(config)

