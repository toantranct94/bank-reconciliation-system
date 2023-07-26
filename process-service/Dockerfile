FROM python:3.10.0-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./app /code/app
# Install Redis and RabbitMQ dependencies
RUN apt-get update && apt-get install -y rabbitmq-server netcat

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY wait-for-rabbitmq.sh /code/wait-for-rabbitmq.sh
RUN chmod +x /code/wait-for-rabbitmq.sh

CMD ["./wait-for-rabbitmq.sh"]
