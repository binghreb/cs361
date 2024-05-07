import pika

def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='message')

    while True:
        mainScreen(channel)
        def callback(ch, method, properties, body):
            print("")
            print(body.decode("utf-8"))

            if((body.decode("utf-8")).startswith("You've selected this product:")):
                quantity = input("Quantity: ")
                while (quantity == "0"):
                    print("Are you sure you would like to cancel this order and return to the main menu? (Yes/No)")
                    answer = input()
                    if(answer.lower() == "yes"):
                        print("")
                        mainScreen(channel)
                    else:
                        print(body.decode("utf-8"))
                        quantity = input("Quantity: ")
                mainScreen(channel)
                    
            if((body.decode("utf-8")).startswith("Whoops! We couldn't find that product.")):
                message = input("Product number/name: ")
                if (message == "0"):
                    print("")
                    mainScreen(channel)
                else:
                    channel.basic_publish(exchange='', routing_key='product', body=message) 
                #mainScreen(channel)
                
            if((body.decode("utf-8")).startswith("Here is the list of products:")):
                print("")
                mainScreen(channel)
            

        channel.basic_consume(queue='products', on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
        


#connection.close()

def mainScreen(channel):
    print("Welcome to paper supply ordering! You can review products, select products, and place orders. Select an option below by entering the associated number.")
    print("   1. List Products")
    print("   2. Select Product to Order")

    option = input("Selection: ")
    
    if(option == "2"):
            selectProduct(channel, option)
    elif(option == "1"):
            listProducts(channel, option)
    else:
        print("Oops! Invalid option. Try again.")
        print("")
        mainScreen(channel)


def selectProduct(channel, option):
    print("Please enter the product number or product name of the product you would like to order.")
    print("To cancel, enter 0.")

    message = input("Product number/name: ")

    if (message == "0"):
        print("")
        mainScreen(channel)
    else:
        channel.basic_publish(exchange='', routing_key='product', body=message) 

def listProducts(channel, option):
    channel.basic_publish(exchange='', routing_key='message', body=option)
    print("")
    #mainScreen(channel)

if __name__ == '__main__':
    main()