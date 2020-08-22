# Import the desired python environment
FROM python:3.8-alpine
# Set the optional maintainer label - replaces deprecated MAINTAINER
LABEL maintainer="Christian Albert"

# Setting the PYTHONUNBUFFERED flag to prevent Python from buffering data
ENV PYTHONUNBUFFERED 1

# Copy the requirements list from project root to Docker image root
COPY ./requirements.txt /requirements.txt
# Install the PostgreSQL client on the Docker system
RUN apk add --update --no-cache postgresql-client jpeg-dev
# Install some temporary dependencies needed for installation
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
# Install all packages from requirements.txt file using pip
RUN pip install -r /requirements.txt
# Delete the temporary dependencies
RUN apk del .tmp-build-deps

# Create empty app directory on Docker image and make it the working directory
RUN mkdir /app
WORKDIR /app
# Copy the content of the project app dir to the app dir on Docker image
COPY ./app /app

# Create new directories for static and media files
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

# Create user to run the application on Docker image to limit the scope
# The -D option for defaults means that user can only run applications
RUN adduser -D user

# Set ownership and permissions to the new directories
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web

# Set the Docker user to user
USER user
