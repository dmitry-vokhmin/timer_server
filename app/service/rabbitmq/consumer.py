import requests
import json

import pika

process = None


def start_consumer():
    def open_url(ch, method, properties, body):
        url = json.loads(body)
        print(url)
        requests.post(url)

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.basic_consume(queue='timer', on_message_callback=open_url, auto_ack=True)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    finally:
        channel.close()
