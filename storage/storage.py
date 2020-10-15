#! bin/python3
import json
import math
import os

import cv2
import numpy
import pika
import webcolors


def store_images(name, colour, image):
    '''Store image to directory according to its average colour.'''
    # create directory for colour if it doesn't exist
    if not os.path.isdir(colour):
        os.mkdir(colour)

    cv2.imwrite(os.path.join(colour, name), image)
    print(f'Stored image "{name}" to directory: "{colour}"')


def validate(data):
    try:
        img_name, img_array, colour = data
    except ValueError:
        return None, None, None

    # check if data are not empty
    if not (img_name and img_array and colour):
        return None, None, None

    # check if data have correct type
    if not (isinstance(img_name, str) and isinstance(img_array, list) and isinstance(colour, list)):
        return None, None, None

    # reform the flattened array
    img = numpy.array(img_array)

    # check if array has expected shape
    if len(img.shape) != 3:
        return None, None, None

    # check if colour has correct format
    if len(colour) != 3 or not all(isinstance(el, int) for el in colour) or any(el > 255 for el in colour):
        return None, None, None

    return img_name, img, colour


def get_closest_colour(colour):
    '''Find closest known colour to the colour given by parameter.'''
    col_distances = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(colour, webcolors.hex_to_rgb(key))]))
        col_distances[distance] = name

    return col_distances[min(col_distances.keys())]


def get_colour_name(colour):
    '''Translate given RGB colour into it's name.
    If name cannot be found, return closest known colour.
    '''
    try:
        name = webcolors.rgb_to_name(colour)
    except ValueError:
        name = get_closest_colour(colour)

    return name


def callback(ch, method, properties, body):
    img_name, img, colour = validate(json.loads(body))
    if img is None:
        print('Received invalid data.')

    print(f'Received data for image: {img_name}')
    colour_name = get_colour_name(colour)

    store_images(img_name, colour_name, img)


if __name__ == "__main__":
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.basic_consume(queue='colours', on_message_callback=callback, auto_ack=True)

    channel.start_consuming()
