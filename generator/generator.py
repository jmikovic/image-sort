#! bin/python3
import argparse
import json
import os
import sys

import cv2
import pika


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='Directory containing images.')
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_arguments()
    image_directory = args.dir

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='images')

    if not os.path.isdir(image_directory):
        print(f"'{image_directory}' is not a directory.")
        sys.exit()

    for img_file in os.listdir(image_directory):
        img = cv2.imread(os.path.join(image_directory, img_file))
        if img is not None:
            img = img.tolist()
            channel.basic_publish(exchange='', routing_key='images', body=json.dumps((img_file, img)))

    channel.close()
