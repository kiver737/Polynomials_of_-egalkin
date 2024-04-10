# Use the official Python 3.11 image as a base image
FROM python:3.11-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements.txt file into our working directory /app
COPY requirements.txt ./

# Install the Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application from your project folder into the container
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define the environment variable for Flask to find the main file
ENV FLASK_APP=flask/app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the Flask application
CMD ["flask", "run"]
