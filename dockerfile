# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Install libpq-dev and gcc
RUN apt-get update && apt-get install -y libpq-dev gcc

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Expose port 8000 for the Django application
EXPOSE 8000

# Define the command to run your Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
