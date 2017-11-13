import logging

from celery import task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)
logger.setLevel(logging.INFO)


@task(queue='silver_giggle.consumer')
def log(message):
    logger.info('Received {}'.format(message))


@task(queue='silver_giggle.consumer')
def fake_log(message):
    logger.info('Received {}'.format(message))
