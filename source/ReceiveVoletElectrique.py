import os
import pika
import VoletElectrique
import json
import time
from types import SimpleNamespace

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    
    monVoletElectrique = VoletElectrique.VoletElectrique()

    channel.queue_declare(queue='lightSensor')

    def callback(ch, method, properties, body):
        value = json.loads(body, object_hook=lambda d: SimpleNamespace(**d))
        print(f" [x] Received : {value.luxVal}")
        if value.luxVal >= 500:
            monVoletElectrique.Open()
        else:
            monVoletElectrique.Close()
        print(f" [x] Volet state: {monVoletElectrique.GetOpen()}")

    channel.basic_consume(queue='lightSensor', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages...')
    channel.start_consuming()

if __name__ == '__main__':
    main()
