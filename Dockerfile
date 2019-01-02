FROM ubuntu:16.04

RUN apt-get update && apt-get install -y git python3-dev curl netcat python3-pip

RUN curl -SL 'https://bootstrap.pypa.io/get-pip.py' | python3
RUN pip install --upgrade pip

RUN mkdir -p /usr/src/app
COPY requirements.txt /usr/src/app
RUN pip install -r /usr/src/app/requirements.txt

WORKDIR /usr/src/app
COPY . /usr/src/app

EXPOSE 8000
