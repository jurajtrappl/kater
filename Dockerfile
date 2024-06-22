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
