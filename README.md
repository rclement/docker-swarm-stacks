# Docker Swarm Stacks

## Requirements

- `python3`
- `pipenv`
- `docker`
- `docker-machine`

## Setup

```
pipenv install -d
pipenv shell
```

## Create a stack

A stack folder follows the files convention:

- `docker-compose.yml`: description of the Docker Swarm stack
- (optional) `.env.example`: required environment variables as example
- `.env`: implementation of `.env.example` (ignored by `git`), required if `.env.example` is present
- (optional) `.secret.example`: required secure variables as example
- `.secret`: implementation of `.secret.example` (ignored by `git`), required if `.secret.example` is present

A few stacks are already using all of the above features.

## Manage a stack

1. If stack directory has a `.env.example` file: copy to `.env` and edit appropriately

2. If stack directory has a `.secret.example` file: copy to `.secret` and edit appropriately

3. Make sure the `docker` client is connected to the remote host:

```
eval $(docker-machine env <host>)
docker node ls
```

4. Deploy the stack (environment variables and secrets will be automatically applied):

```
inv stack-up -s <stack> -m <mode1,mode2>
```

5. Take-down the stack:

```
inv stack-down -s <stack>
```

## License

The MIT License (MIT)

Copyright (c) 2018 Romain Clement
