#!/usr/bin/env bash

# Modify this to add custom variables and connections to your installation

# This is the path inside the running container where this script is located
# The mountpoint is set in docker-compose-dev.yml
MOUNT_PATH=/usr/local/airflow/initialize


### Install Variables
###
### Install variables into the airflow database on startup.

airflow variables --import ${MOUNT_PATH}/variables.json


### Configure GCP auth using a service account key
###
### Uncomment below and edit as needed.

#airflow connections --delete --conn_id=google_cloud_default
#airflow connections --add \
#  --conn_id=google_cloud_default \
#  --conn_type=google_cloud_platform \
#  --conn_extra="$(cat ${MOUNT_PATH}/connection.json)"


#gcloud auth activate-service-account --key-file=${MOUNT_PATH}/SERVICE_ACCOUNT.json
#gcloud config set project PROJECT_ID


