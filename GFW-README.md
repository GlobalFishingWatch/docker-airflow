# GFW fork of puckel/docker-airflow

This is a fork of [puckel/docker-airflow](https://github.com/puckel/docker-airflow) and branched
off at tag 1.8.1 which was the last commit that supported python 2

This is intended to serve as a development environment for authoring dags

## Modifications

* Use airflow 1.9.0rc1

## Use

```
docker-compose -f docker-compose-LocalExecutor.yml build
docker-compose -f docker-compose-LocalExecutor.yml up -d
```

Point a browser at
```
http://127.0.0.1:8080
```

The dags folder is mounted from `~/github/docker-airflow/dags` by `docker-compose-LocalExecutor.yml`
Anything you put here will be seen by the airflow server


## TODO
Add docs for google auth.  Maybe mount a service account auth?


 