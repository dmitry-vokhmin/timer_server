import pika

from app.service.rabbitmq import get_queue_connection


class BaseRabbitQueuePublisher:
    queue = 'timer'
    delay_queue = 'timer_delay'

    def __init__(self):
        self.connection = get_queue_connection()
        channel = self.connection.channel()
        channel.queue_declare(queue=self.queue, durable=True)
        channel.queue_bind(exchange='amq.direct',
                           queue=self.queue)
        self.delay_channel = self.connection.channel()
        self.delay_channel.queue_declare(queue=self.delay_queue, durable=True,
                                         arguments={
                                             'x-dead-letter-exchange': 'amq.direct',
                                             'x-dead-letter-routing-key': self.queue
                                         })

    def publish(self, message: str, expiration: int) -> None:
        properties = pika.BasicProperties(
            delivery_mode=2, expiration=str(expiration))
        self.delay_channel.basic_publish(
            exchange='',
            routing_key=self.delay_queue,
            body=message,
            properties=properties
        )
