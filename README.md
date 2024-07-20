# kater
Medieval game that we will fall in love with.

https://jurajtrappl.github.io/kater/

Run:

docker compose up kater-xming

pygbag .

python main.py

### Server
//docker build -f Dockerfile-server --target kater-be --progress=plain --no-cache -t be   
docker compose -f docker-compose-server.yml build --no-cache backend