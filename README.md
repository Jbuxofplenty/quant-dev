# Python Live Algorithm Trading

## General commands

---

### Deploying
>Deploy new algorithm, after changes are made to algo.py
```
heroku login
git add -A
git commit -am "New Algorithm"
git push heroku master
heroku ps:scale worker=1 -a quant-dev
```

>Set git to remote heroku
```
heroku git:remote -a quant-dev
```

>Test deploy first
```
heroku local
```

### Logging
>View logs of heroku app
```
heroku logs --tail -a quant-dev
```



### Configuration
>View configuration settings
```
heroku config -a quant-dev
```

>Set environment variables
```
heroku config:set -a quant-dev APCA_API_BASE_URL=https://paper-api.alpaca.markets
```

>Ensure heroku instance is set to a container
```
heroku stack:set container -a quant-dev
```

### Docker functions

>Build an image
```
docker build -t quant-dev --build-arg APCA_API_KEY_ID=$APCA_API_KEY_ID --build-arg APCA_API_SECRET_KEY=$APCA_API_SECRET_KEY --build-arg APCA_API_BASE_URL=$APCA_API_BASE_URL  .
```

>View images
```
docker images
```

>Remove an image
```
docker image remove quant-dev
```

>View containers
```
docker container ls -a
```

>Delete a container
```
docker container rm quant-dev
```

>Remove all stopped containers
```
docker container prune
```

>Run a docker container with an interactive shell
```
docker run -it quant-dev sh
```


## Initial Setup

---
### Github Setup

> algo.py
```
Example here: https://github.com/alpacahq/pylivetrader/blob/master/examples/MACD/macd_example.py
```

>Dockerfile
```
FROM alpacamarkets/pylivetrader
ARG APCA_API_SECRET_KEY
ARG APCA_API_KEY_ID
ARG APCA_API_BASE_URL
ENV APCA_API_SECRET_KEY=$APCA_API_SECRET_KEY
ENV APCA_API_KEY_ID=$APCA_API_KEY_ID
ENV APCA_API_BASE_URL=$APCA_API_BASE_URL
RUN mkdir /app
COPY . /app
WORKDIR /app
CMD pylivetrader run -f algo.py
```

> heroku.yml
```
build:
  config:
    APCA_API_KEY_ID: $APCA_API_KEY_ID
    APCA_API_SECRET_KEY: $APCA_API_SECRET_KEY
  docker:
    worker: Dockerfile
run:
  worker:
    image: worker
```

Push repository to github.com (follow instructions there if needed)

---

### Heroku Setup

1. Login (create account if needed)
2. Create New App (New > Create App)
3. Find 'Deployment method' on 'Deploy' tab
4. Choose Github and connect
5. Once initial deploy completes see 'Resources' tab and enable the worker (see above)
7. Update Config Vars with (see above)

```
APCA_API_SECRET_KEY = {{YOUR APCA_API_SECRET_KEY}}
APCA_API_KEY_ID = {{YOUR APCA_API_KEY_ID}}
APCA_API_BASE_URL = {{APCA_API_BASE_URL paper-api.alpaca.markets or api.alpaca.markets}}
```

>Heroku brew installation (OSX)
```
brew tap heroku/brew && brew install heroku
```

>Homebrew installation (OSX)
```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
