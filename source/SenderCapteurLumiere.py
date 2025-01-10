import os
import pika
import CapteurLumiere
import json

monCapteurLumiere = CapteurLumiere.CapteurLumiere()
luxVal = monCapteurLumiere.createRandomLux()

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='lightSensor')

data_dict = {'luxVal': luxVal}
to_json = json.dumps(data_dict)

channel.basic_publish(exchange='', routing_key='lightSensor', body=to_json)
print(" [x] Sent lux value : " + str(luxVal) + "")
connection.close()
