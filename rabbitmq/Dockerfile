FROM rabbitmq:3.8-management

ENV RABBITMQ_USER guest
ENV RABBITMQ_PASSWORD guest

ADD rabbitmq.conf /etc/rabbitmq/
ADD definitions.json /etc/rabbitmq/

RUN chown rabbitmq:rabbitmq /etc/rabbitmq/rabbitmq.conf /etc/rabbitmq/definitions.json

