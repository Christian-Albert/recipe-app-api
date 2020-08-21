# Import the desired python environment
FROM python:3.8-alpine
# Set the optional maintainer label - replaces deprecated MAINTAINER
LABEL maintainer="Christian Albert"

# Setting the PYTHONUNBUFFERED flag to prevent Python from buffering data
ENV PYTHONUNBUFFERED 1

# Copy the requirements list from project root to Docker image root
COPY ./requirements.txt /requirements.txt
# Install all packages fromrequirements.txt file
RUN pip install -r /requirements.txt

# Create empty app directory on Docker image and make it the working directory
RUN mkdir /app
WORKDIR /app
# Copy the content of the project app dir to the app dir on Docker image
COPY ./app /app

# Create user to run the application on Docker image to limit the scope
# The -D option for defaults means that user can only run applications
RUN adduser -D user
# Set the Docker user to user
USER user
