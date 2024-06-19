FROM python:3.10

WORKDIR /app

COPY . ./

RUN /app/install.sh

ENV DISPLAY=host.docker.internal:0.0

CMD [ "python", "main.py", "--character_save", "example_players/player1"]
