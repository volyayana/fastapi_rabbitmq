# FastAPI with RabbitMQ Integration

This is an example application demonstrating the integration of FastAPI with RabbitMQ using the aio-pika library. The application sets up a main queue where regular messages are received. If messages remain in the main queue longer than a specified period, they are automatically moved to the dead queue for further troubleshooting.

## Setup

1. **Clone the Repository:** 
   ```bash
   git clone https://github.com/volyayana/fastapi_rabbitmq.git

2. **Install Dependencies:**
Navigate to the project directory and install the required dependencies using pip:
    ```bash
    pip install -r requirements.txt

3. **Configuration:**
Update the configuration settings in .env.example and rename it to .env


## Running the Application
Run the FastAPI application:

    python start.py

The application will start at http://127.0.0.1:8000.

## Swagger
Auto-generated documentation will be available via endpoint http://127.0.0.1:8000/docs.

## Message Handling
Messages are initially published to the main queue.
If a message remains in the main queue longer than the specified time-to-live (variable MESSAGE_TTL, in seconds), it is automatically moved to the dead queue for further troubleshooting.

## Monitoring
You can monitor the RabbitMQ queues using the RabbitMQ Management Console.

Access the RabbitMQ Management Console at http://localhost:15672 (default credentials: guest/guest).