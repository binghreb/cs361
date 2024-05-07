import pika, sys, os
import csv

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='message')
    channel.queue_declare(queue='products')

    def callback(ch, method, properties, body):
         
         if (body.decode("utf-8") == "1"):
        
            products = ""
            with open('products.csv', newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                for row in spamreader:
                    products +=  "\n" + str(row[0]).replace(",", " : ")
            
            message = ("Here is the list of products: " + products)
            channel.basic_publish(exchange='', routing_key='products', body=message) 

    channel.basic_consume(queue='message', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages.')
    channel.start_consuming()

    

if __name__ == '__main__':
    main()