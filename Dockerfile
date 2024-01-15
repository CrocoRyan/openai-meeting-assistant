# Use ffmpeg:4.3-alpine as the base image
FROM ffmpeg:4.3-alpine

# Install Python 3.8 and pip
RUN apk add --no-cache python3=3.8 py3-pip

# Upgrade pip
RUN pip3 install --upgrade pip

# The rest of your Dockerfile follows...
# For example, copy your application code and install Python dependencies
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

# Your application's specific commands follow...
CMD ["python", "app.py"]
