from datetime import timedelta

from kombu import Exchange, Queue

from silver_giggle.celery import init_celery


def init_producer():
    app = init_celery('producer', 'silver_giggle.producer')

    channel = app.broker_connection().channel()

    broadcast_exchange = Exchange('silver_giggle.producer.broadcast', channel=channel)
    broadcast_exchange.declare()

    app.conf.task_queues = (
        Queue('silver_giggle.producer.broadcast', broadcast_exchange),
        Queue('silver_giggle.producer', Exchange('silver_giggle.producer')),
    )

    app.conf.task_routes = {
        'silver_giggle.producer.tasks.log': 'silver_giggle.producer',
        'silver_giggle.consumer.tasks.log': {
            'queue': 'silver_giggle.producer.broadcast',
            'exchange': 'silver_giggle.producer.broadcast',
            'routing_key': 'msg'
        }
    }

    app.conf.beat_schedule = {
        'log': {
            'task': 'silver_giggle.producer.tasks.log',
            'schedule': timedelta(seconds=1),
            'args': (),
        }
    }

    return app


# producer celery app
app = init_producer()
