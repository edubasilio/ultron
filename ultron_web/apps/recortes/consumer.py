#!/usr/bin/env python3
import pika, sys, os, ast

from .models import Recorte


def main():
    credentials = pika.PlainCredentials('basilio', 'basilio')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='celery', durable=True)

    def callback(ch, method, properties, body):
        body = body.decode()
        body = body.replace('[[{', '{')
        body = body.replace('{},', '')
        body = body.replace('}]]', '}')
        body = body.replace('null', 'None')
        body = ast.literal_eval(body)
        body = body[:-1]

        ids = [r.get('id') for r in body if type(r) == dict]

        recortes = Recorte.objects.filter(id__in=ids)
        print(recortes)

    channel.basic_consume(queue='celery', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

# if __name__ == '__main__':
#     try:
#         main()
#     except KeyboardInterrupt:
#         print('Interrupted')
#         try:
#             sys.exit(0)
#         except SystemExit:
#             os._exit(0)