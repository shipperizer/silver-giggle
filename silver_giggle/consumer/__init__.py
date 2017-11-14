from os import environ

from kombu import Exchange, Queue

from silver_giggle.celery import init_celery


def init_consumer():
    app = init_celery('consumer.{}'.format(environ['CELERY_NAME']), 'silver_giggle.consumer')

    app.conf.task_queues = [
        Queue('{}.msg'.format(app.main), Exchange('silver_giggle.producer.broadcast'), routing_key='msg'),
        Queue('{}.fake.msg'.format(app.main,), Exchange('silver_giggle.producer.broadcast'), routing_key='fake'),
    ]

    return app


# consumer celery app
app = init_consumer()
