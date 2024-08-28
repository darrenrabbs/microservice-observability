# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install curl and other dependencies
RUN apt-get update && apt-get install -y curl

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the test script and the entrypoint script into the container
COPY test_metrics.py .
COPY entrypoint.sh .

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

# Use the entrypoint script to run the tests
ENTRYPOINT ["./entrypoint.sh"]