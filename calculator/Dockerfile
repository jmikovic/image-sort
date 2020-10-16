FROM python:3

RUN pip install numpy pika

ADD . /root/src
RUN chmod 0755 /root/src/calculator.py

CMD python /root/src/calculator.py
