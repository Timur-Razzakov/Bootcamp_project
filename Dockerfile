FROM python:3.8
RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean

# create work dir
RUN mkdir /app
# Define work dir
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy reqs
COPY ./requirements.txt .
# Install reqs
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt


# Copy all stuff
COPY . /app

## Run python  manage.py
#CMD python manage.py runserver