# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 5000


# Define environment variable
ENV NAME AWS_IAM_APP

# Set PYTHONPATH to the src directory
ENV PYTHONPATH "${PYTHONPATH}:/app/src"

# Run main.py when the container launches
CMD ["python", "src/main.py"]