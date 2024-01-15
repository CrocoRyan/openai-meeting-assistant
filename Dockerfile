# Use ffmpeg:4.3-alpine as the base image
FROM ubuntu:20.04

# production profile
ENV FLASK_ENV=prod
ENV FLASK_DEBUG=true
# Install Python 3.8 and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*


RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE > /etc/timezone
RUN apt-get update -y && apt-get install -y ffmpeg
# Upgrade pip
#RUN pip3 install --upgrade pip
#
#RUN python3 --version
RUN mkdir /app

WORKDIR /app

# Add a dummy file to trigger Docker to consider this step changed

# Copy everything from the current directory to the working directory in the image
COPY . .


RUN pip3 install -r /app/requirements.txt
EXPOSE 5000
# Your application's specific commands follow...
CMD ["python3", "run.py"]
