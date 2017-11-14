import logging

from celery import task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)
logger.setLevel(logging.INFO)


@task
def log(message):
    logger.info('Received {}'.format(message))


@task
def fake(message):
    logger.info('Received fake {}'.format(message))
