FROM python:3

RUN pip install pika opencv-python

ADD . /root/src
RUN chmod 0755 /root/src/generator.py

CMD tail -f /dev/null
