#!/bin/bash

# Wait for RabbitMQ to be ready
while ! nc -z rabbitmq 5672; do
  echo "Waiting for RabbitMQ to start..."
  sleep 2
done

echo "RabbitMQ is up and running. Starting the Python application."
cd app
exec python main.py
