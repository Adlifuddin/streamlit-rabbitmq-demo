import pika
import json
import pandas as pd
from crawler import crawler

try:
    parameters = pika.ConnectionParameters(host='localhost')
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    channel.queue_declare(queue='crawler')

    def on_request(ch, method, props, body):

        data = json.loads(body)

        result = crawler(data)

        ch.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(
                correlation_id = props.correlation_id,
                content_type="application/json",
                delivery_mode=2
            ),
            body=json.dumps(result)
        )

        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=2)

    channel.basic_consume(queue='crawler', on_message_callback=on_request)

    print("[x] Awaiting Crawler Tasks")
    channel.start_consuming()

except KeyboardInterrupt:
    pass