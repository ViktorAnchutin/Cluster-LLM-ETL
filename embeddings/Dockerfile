# Use the official Python image with version 3.10
FROM  python:3.10

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the working directory in the container
WORKDIR /app

COPY embeddings_load.py .

# Create a directory for data in the container
RUN mkdir data

# Specify the command to run on container start with CMD

ENTRYPOINT ["python", "embeddings_load.py"]
