# Local Docker Swarm cluster demo

1. Create Swarm cluster

```
    docker-machine create --driver virtualbox --virtualbox-hostonly-cidr "10.0.0.20/24" cluster-master
    docker-machine create --driver virtualbox --virtualbox-hostonly-cidr "10.0.0.20/24" cluster-worker-1
    docker-machine create --driver virtualbox --virtualbox-hostonly-cidr "10.0.0.20/24" cluster-worker-2
    docker-machine ls

    docker-machine ssh cluster-master "docker swarm init --advertise-addr 10.0.0.100"
    docker-machine ssh cluster-worker-1 "docker swarm join --token <token> 10.0.0.100:2377"
    docker-machine ssh cluster-worker-2 "docker swarm join --token <token> 10.0.0.100:2377"
```

2. Remote control cluster

```
    eval $(docker-machine env cluster-master)
    docker-machine ls
    docker node ls
    docker stack ls
    docker service ls
    docker secret ls
    eval $(docker-machine env -u)
```

3. Deploy stacks

```
    inv stack-deploy -s traefik
    inv stack-deploy -s portainer
    inv stack-deploy -s matomo
    inv stack-deploy -s mailer
```

4. Edit `/etc/hosts`:

```
    10.0.0.100  docker.me
    10.0.0.100  traefik.docker.me
    10.0.0.100  portainer.docker.me
    10.0.0.100  matomo.docker.me
    10.0.0.100  mailer.docker.me
```

5. Send mail:

```
    http -v POST http://mailer.docker.me/api/mail \
        subject='Surprise, surprise...' \
        message='Happy 6th Birthday, Docker! 🎉' \
        email='docker@grenoble.io' \
        name='Docker Grenoble' \
        honeypot=''
```

6. Destroy stacks

```
    inv stack-destroy -s mailer
    inv stack-destroy -s matomo
    inv stack-destroy -s portainer
    inv stack-destroy -s traefik
```
