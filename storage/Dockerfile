FROM python:3

RUN pip install pika opencv-python numpy webcolors

ADD . /root/src
RUN chmod 0755 /root/src/storage.py

CMD python /root/src/storage.py
