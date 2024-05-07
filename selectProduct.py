import pika, sys, os
import csv

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='product')
    channel.queue_declare(queue='products')

    def callback(ch, method, properties, body):
        
        message = findProduct(body.decode("utf-8"))
        channel.basic_publish(exchange='', routing_key='products', body=message) 

    channel.basic_consume(queue='product', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages.')
    channel.start_consuming()

def findProduct(productSelection):
    message = "Whoops! We couldn't find that product. Try another product name/number, or enter 0 to return to the main menu."
    with open('products.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                products = str(row[0]).split(",")
                if (products[0] == productSelection or products[1] == productSelection):
                    message = ("You've selected this product: " + products[1])
    return message


if __name__ == '__main__':
    main()