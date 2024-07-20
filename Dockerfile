FROM python:3.12 as docker-xming

WORKDIR /app

COPY . ./

RUN pip install -r requirements.txt

ENV DISPLAY=host.docker.internal:0.0

CMD [ "python", "main.py"]



FROM python:3.12 as docker-web

RUN apt-get -y update && apt install -y ffmpeg

WORKDIR /app

COPY . ./

RUN pip install -r requirements.txt

CMD [ "pygbag", "--bind", "0.0.0.0", "."]


# syntax=docker/dockerfile:1.4

FROM --platform=$BUILDPLATFORM python:3.12.3-slim AS kater-be
EXPOSE 8000

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc \
       libpq-dev \
       build-essential \
       curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app 
COPY /backend/kater/requirements.txt /app
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir
COPY /backend/kater /app 
RUN ls -l
ENTRYPOINT ["python3"] 
CMD ["manage.py", "runserver", "0.0.0.0:8000"]
