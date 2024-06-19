FROM python:3.10

WORKDIR /app

COPY . ./

RUN /app/install.sh
RUN mkdir /app/saved
ENV DISPLAY=host.docker.internal:0.0

#CMD [ "python", "src/main.py", "--character_save", "example_players/player1"]
CMD [ "python", "src/main.py"]
