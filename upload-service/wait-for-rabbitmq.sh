#!/bin/bash

# Wait for RabbitMQ to be ready
while ! nc -z rabbitmq 5672; do
  echo "Waiting for RabbitMQ to start..."
  sleep 2
done

echo "RabbitMQ is up and running. Starting the Python application."
exec uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
