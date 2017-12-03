# GFW fork of puckel/docker-airflow

This is a fork of [puckel/docker-airflow](https://github.com/puckel/docker-airflow) and branched
off at tag 1.8.1 which was the last commit that supported python 2

This is intended to serve as a development environment for authoring dags

## Modifications

* Use airflow 1.9.0rc1
* Modify entrypoint.sh to provide optional initialization of variables and connections on startup
* Add docker-in-docker support to Dockerfile
* add gcloud to Dockerfile
* run as root instead of airflow server to support docker-in-docker

## Setup

In order to use GCP hooks in airflow (like dataflow), you need to have GCP auth inside the
container.  To do this, we mount a named volume `gcp` into /root/.config and then perform 
authentication inside the container.  This needs to be done only once

```
docker volume create --name=gcp
docker-compose -f docker-compose-dev.yml build
cp -r ./initialize-template /initialize
```

Run the contianer with 
```
docker-compose -f docker-compose-dev.yml up -d
```

Point a browser at
```
http://127.0.0.1:8080
```

The dags folder is mounted from `~/github/docker-airflow/dags` by `docker-compose-LocalExecutor.yml`
Anything you put here will be seen by the airflow server

## Docker in Docker

We are running airflow here in a docker container, and inside the airflow dag files, we want to run 
piplines which are also packaged in docker containers.  This means we neeed to run docker inside docker.

We have two issues that needs to be addressed to make this work.  

First, we have to allow docker containers using the docker environemnt on the host machine, so we have to 
expose that inside the airflow container.  We do this in the docker-compose yaml file with 

```
        volumes:
             - /var/run/docker.sock:/var/run/docker.sock
```

The second issue is exposing the GCP auth configuration to the inner container without having to initialize it.

## GCP Authentication

We share gcp auth context by mounting a named volume inside the airflow container at /root/.config and then
we expose the same (external) named volume to the inner container.  This is accomplished in the docker-compose 
yaml file with 

```
services:
    webserver:
         volumes:
             - gcp:/root/.config/

volumes:
  gcp:
    external: true

```


or with 
```
docker run -v gcp:/root/.config/ [IMAGE]
```





 