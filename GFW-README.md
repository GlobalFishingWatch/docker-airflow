# GFW fork of puckel/docker-airflow

This is a fork of [puckel/docker-airflow](https://github.com/puckel/docker-airflow) and branched
off at tag 1.8.1 which was the last commit that supported python 2

This is intended to serve as a development environment for authoring dags

## Modifications

* Use airflow 1.10.0 (November 2018)

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


## Testing pipelines

For testing the airflow portion of an installable pipeline, it is convenient to mount the 
dag folder directly into the docker-airflow container instead of installing it from the pipeline
docker image.  This allows you to edit the dags files in place and debug.

To run a pipeline this way, edit the `.env` file and put in the name of the pipeline and 
the path to the airflow folder that contains the pipeline dags

Then you can use `docker-compose-test.yaml` to bring up the airflow container and the pipeline 
will be mounted into the dags folder an it's post_install script will be run on startup

There are also convenience scripts which use this compose file

  up.sh
  down.sh 
  exec_bash.sh



## TODO
Add docs for google auth.  Maybe mount a service account auth?


 
