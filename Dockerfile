# Use the official Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the application files to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Install a simple HTTP server
RUN pip install flask

# Expose the port your app runs on
EXPOSE 8000

# Start the application
CMD python3 -u health_check.py & python3 bot.py
