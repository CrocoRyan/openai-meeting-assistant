# Stage 1: Get FFmpeg from the official image
FROM jrottenberg/ffmpeg:4.1-alpine as ffmpeg

# Stage 2: Set up the Python environment
FROM python:3.8-alpine

# Copy FFmpeg bins from the first stage
COPY --from=ffmpeg /usr/local /usr/local

# Set a working directory for your application
WORKDIR /app

# Install any additional dependencies (if necessary)
RUN apk update && \
    apk add --no-cache gcc musl-dev

# Copy the requirements.txt file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your Flask application's code to the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Set the default command to run your app
CMD ["python", "app.py"]
