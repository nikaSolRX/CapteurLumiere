import os
import pika
import mysql.connector
import json
from types import SimpleNamespace

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    
    channel.queue_declare(queue='lightSensor')

    def callback(ch, method, properties, body):
        value = json.loads(body, object_hook=lambda d: SimpleNamespace(**d))
        print(f" [x] Received : {value.luxVal}")

        mydb = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user='root',
            password='root',
            database='LightSensorProject'
        )
        
        mycursor = mydb.cursor()
        sql = "INSERT INTO LUX (val) VALUES (%s)"
        mycursor.execute(sql, (value.luxVal,))
        mydb.commit()
        print(f" [x] Inserted into DB: {value.luxVal}")

    channel.basic_consume(queue='lightSensor', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages...')
    channel.start_consuming()

if __name__ == '__main__':
    main()
