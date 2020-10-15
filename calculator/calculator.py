#! bin/python3
import json
import numpy
import pika


def calculate_colour(image):
    '''calculate average colour of received image'''
    avg_per_row = numpy.average(image, axis=0)
    avg_colour = numpy.average(avg_per_row, axis=0)

    # round off average values and turn the order to RGB
    colour = numpy.array(numpy.rint(avg_colour), dtype=numpy.uint8)[::-1]

    return colour.tolist()


def validate(data):
    try:
        img_name, img_array = data
    except ValueError:
        return None, None, None

    # ensure data are not empty
    if not (img_array and img_name):
        return None, None, None

    # check if data have correct type
    if not (isinstance(img_name, str) and isinstance(img_array, list)):
        return None, None, None

    # reform the flattened array
    img = numpy.array(img_array)

    # check if array has expected shape
    if len(img.shape) != 3:
        return None, None, None

    return img_name, img_array, img


def callback(ch, method, properties, body):
    img_name, img_array, img = validate(json.loads(body))
    if img is None:
        print('Received invalid data.')
        return

    print(f'Received data for image: {img_name}')
    colour = calculate_colour(img)
    payload = json.dumps((img_name, img_array, colour))
    channel.basic_publish(exchange='', routing_key='colours', body=payload)
    print(f'Sent image "{img_name}" with average colour: "{colour}"')


if __name__ == "__main__":
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='colours')
    channel.basic_consume(queue='images', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
